from .. import db
from ..database import Solutions, Results, Games

class Modeling():
    Game = None
    Current_period_solution = None
    Current_period_result = None
    Previous_solutions = None
    Previous_results = None
    Current_period = None

    def __init__(self, current_user, form):
        self.Current_period = form['period']
        self.Game = Games.query.filter_by(id=current_user.game_id).first()
        self.Previous_solutions = db.session.query(Solutions).filter(Solutions.gamer_id == current_user.id).all()
        self.Previous_results = db.session.query(Results).filter(Results.gamer_id == current_user.id).all()
        self.Current_period_solution = Solutions.query.filter_by(period_id=form['period'], gamer_id=current_user.id).first()
        if self.Current_period_solution is None:
            self.Current_period_solution = Solutions(form=form, game=self.Game, gamer_id=current_user.id)
            self.Current_period_result = Results()
            self.generateResult()
            self.Current_period_result.gamer_id = current_user.id
        else:
            self.Current_period_solution.recount(form, self.Game)
            self.Current_period_result = db.session.query(Results).\
                filter_by(solutions_id=self.Current_period_solution.id).\
                first()
            self.generateResult()
        db.session.add(self.Current_period_solution)
        db.session.flush()
        db.session.refresh(self.Current_period_solution)
        self.Current_period_result.solution_id=self.Current_period_solution.id
        db.session.add(self.Current_period_result)

    def generateResult(self):

        self.Current_period_result.period_id = self.Current_period

        quality_cost_acc = int(self.Game.quality_cost_base) + int(self.Current_period_solution.niokrQuality)
        prime_cost_acc = int(self.Game.prime_cost_base) + int(self.Current_period_solution.niokrSS)

        for solution in self.Previous_solutions:
            quality_cost_acc += int(solution.niokrQuality)
            prime_cost_acc += int(solution.niokrSS)

        mult_Quality = (quality_cost_acc / int(self.Game.quality_cost_base)) ** (1 / int(self.Game.quality_cost_coef))
        mult_Price = 1 / (int(self.Game.price_coef) ** (int(self.Current_period_solution.cost) - int(self.Game.cost_min)))

        self.Current_period_result.Sales = 0
        if self.Game.NAPromotion_active is True:
            self.Current_period_result.mult_Demand_NA = mult_Price * mult_Quality * float(self.Current_period_solution.NAPromotion)
            sum_mult_Demand_NA = self.Current_period_result.mult_Demand_NA
            for result in self.Previous_results:
                sum_mult_Demand_NA += self.Current_period_result.mult_Demand_NA
            try:
                self.Current_period_result.Demand_NA = int(self.Game.sizeNA) * self.Current_period_result.mult_Demand_NA / sum_mult_Demand_NA
            except ZeroDivisionError:
                self.Current_period_result.Demand_NA = 0
            self.Current_period_result.Sales_NA = min([ self.Current_period_result.Demand_NA, float(self.Current_period_solution.NAFactory)])
            self.Current_period_result.Sales += self.Current_period_result.Sales_NA
        if self.Game.EuropePromotion_active is True:
            self.Current_period_result.mult_Demand_Europa = mult_Price * mult_Quality * float(self.Current_period_solution.EuropePromotion)
            sum_mult_Demand_Europa =  self.Current_period_result.mult_Demand_Europa
            for result in self.Previous_results:
                sum_mult_Demand_Europa += self.Current_period_result.mult_Demand_Europa
            try:
                self.Current_period_result.Demand_Europa = int(self.Game.sizeEurope) * self.Current_period_result.mult_Demand_Europa / sum_mult_Demand_Europa
            except:
                self.Current_period_result.Demand_Europa = 0
            self.Current_period_result.Sales_Europa = min([self.Current_period_result.Demand_Europa, float(self.Current_period_solution.EuropeFactory)])
            self.Current_period_result.Sales +=  self.Current_period_result.Sales_Europa
        if self.Game.AsiaPromotion_active is True:
            self.Current_period_result.mult_Demand_Asia = mult_Price * mult_Quality * float(self.Current_period_solution.AsiaPromotion)
            sum_mult_Demand_Asia = self.Current_period_result.mult_Demand_Asia
            for result in self.Previous_results:
                sum_mult_Demand_Asia += self.Current_period_result.mult_Demand_Asia
            try:
                self.Current_period_result.Demand_Asia = int(self.Game.sizeAsia) * self.mult_Demand_Asia / sum_mult_Demand_Asia
            except:
                self.Current_period_result.Demand_Asia = 0
            self.Current_period_result.Sales_Asia = min([self.Current_period_result.Demand_Asia, float(self.Current_period_solution.AsiaFactory)])
            self.Current_period_result.Sales += self.Current_period_result.Sales_Asia

        self.Current_period_result.Prime_cost = self.Game.prime_cost_start + 1 - (prime_cost_acc / self.Game.prime_cost_base) ** (
        1 / self.Game.prime_cost_coef)

        # Прибыль в периоде
        # self.Profit = (current_solution.cost - self.Prime_cost)*self.Sales-self.Budget
