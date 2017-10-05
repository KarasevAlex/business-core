from .. import db
from ..database import Solutions, Results, Games,Period
class Modeling():
    Game = None
    Current_period_solution = None
    Current_period_result = None
    Previous_solutions = None
    Previous_results = None
    Current_period = None
    def __init__(self,current_user, form):
        self.Current_period = form['period']
        self.Game = Games.query.filter_by(id=current_user.game_id).first()
        self.Current_period_solution = Solutions(form=form, game=self.Game,gamer_id=current_user.id)
        self.Previous_solutions = db.session.query(Solutions).filter(Solutions.gamer_id == current_user.id)
        self.Previous_results = db.session.query(Results).filter(Results.gamer_id == current_user.id)
        Current_period_result = Results()
    def  generateResult(self):
        result = Results()
        quality_cost_acc = int(self.Game.quality_cost_base) + int(self.Current_period_solution.niokrQuality)
        prime_cost_acc = int(self.Game.prime_cost_base) + int(self.Current_period_solution.niokrSS)

        for solution in self.Previous_solutions:
            quality_cost_acc += solution.niokrQuality
            prime_cost_acc += solution.niokrSS

        mult_Quality = (quality_cost_acc / int(self.Game.quality_cost_base)) ** (1 / int(self.Game.quality_cost_coef))
        mult_Price = 1 / int(self.Game.price_coef) ** (int(self.Current_period_solution.cost) - int(self.Game.cost_min))

        result.Sales = 0
        if self.Game.NAPromotion_active is True:
            result.mult_Demand_NA = mult_Price * mult_Quality * float(self.Current_period_solution.NAPromotion)
            sum_mult_Demand_NA = result.mult_Demand_NA
            for result in self.Previous_results:
                sum_mult_Demand_NA += result.mult_Demand_NA
            result.Demand_NA = int(self.Game.sizeNA) * result.mult_Demand_NA / sum_mult_Demand_NA
            result.Sales_NA = min([result.Demand_NA, float(self.Current_period_solution.NAFactory)])
            result.Sales += result.Sales_NA
        if self.Game.EuropePromotion_active is True:
            self.mult_Demand_Europa = mult_Price * mult_Quality * float(self.Current_period_solution.EuropePromotion)
            sum_mult_Demand_Europa = self.mult_Demand_Europa
            for result in self.Previous_results:
                sum_mult_Demand_Europa += result.mult_Demand_Europa
            self.Demand_Europa = int(self.Game.sizeEurope) * self.mult_Demand_Europa / sum_mult_Demand_Europa
            self.Sales_Europa = min([self.Demand_Europa, float(self.Current_period_solution.EuropeFactory)])
            self.Sales += self.Sales_Europa
        if self.Game.AsiaPromotion_active is True:
            self.mult_Demand_Asia = mult_Price * mult_Quality * float(self.Current_period_solution.AsiaPromotion)
            sum_mult_Demand_Asia = self.mult_Demand_Asia
            for result in self.Previous_results:
                sum_mult_Demand_Asia += result.mult_Demand_Asia
            self.Demand_Asia = int(self.Game.sizeAsia) * self.mult_Demand_Asia / sum_mult_Demand_Asia
            self.Sales_Asia = min([self.Demand_Asia, float(self.Current_period_solution.AsiaFactory)])
            self.Sales += self.Sales_Asia

        self.Prime_cost = self.Game.prime_cost_start + 1 - (prime_cost_acc / self.Game.prime_cost_base) ** (
        1 / self.Game.prime_cost_coef)
        # Прибыль в периоде
        # self.Profit = (current_solution.cost - self.Prime_cost)*self.Sales-self.Budget
