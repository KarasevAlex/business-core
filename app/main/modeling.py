from ..database import Solutions, Games, Period
from .. import db

class Modeling():
    Game = None
    Current_period_solution = None
    Current_period_solutions = None
    Previous_solutions = None
    Current_period = None

    def __init__(self, current_user, form):
        self.Current_period = form['period']
        self.Game = Games.query.filter_by(id=current_user.game_id).first()
        self.Previous_solutions = Solutions.query.filter_by()
        self.Current_period_solutions = Solutions.query.filter_by(period_id=form['period']).all()
        if len(self.Current_period_solutions) == 0:
            Sol=Solutions.getPreviousSolutions(self.Current_period)
            for previous_solution in Sol:
                if previous_solution.gamer_id == current_user.id:
                    self.Current_period_solution = Solutions.set_previous(self.Current_period, previous_solution)
                    self.Current_period_solution.update_solution(form)
                    self.Current_period_solution.count_personal_params(self.Game)
                    self.Current_period_solutions.append(self.Current_period_solution)
                else:
                    self.Current_period_solution = Solutions.set_previous(self.Current_period, previous_solution)
                    self.Current_period_solution.count_personal_params(self.Game)
                    self.Current_period_solutions.append(self.Current_period_solution)
                db.session.add(self.Current_period_solution)
        else:
            for previous_solution in self.Current_period_solutions:
                if previous_solution.gamer_id == current_user.id:
                    previous_solution.update_solution(form)
                    previous_solution.count_personal_params(self.Game)

        self.generateResult()
    def getPeriod(self):
        return Period.query.filter_by(id=self.Current_period).firts()
    def getGame(self):
        return self.Game
    def getCurrentSolution(self):
        return  self.Current_period_solution
    def generateResult(self):

        sum_Mult_Demand_NA = 0
        sum_Mult_Demand_Asia = 0
        sum_Mult_Demand_Europe = 0

        for solution in self.Current_period_solutions:
            sum_Mult_Demand_NA += solution.mult_Demand_NA
            sum_Mult_Demand_Asia += solution.mult_Demand_Asia
            sum_Mult_Demand_Europe += solution.mult_Demand_Europa

        for solution in self.Current_period_solutions:
            try:
                solution.Demand_NA = int(self.Game.sizeNA) * solution.mult_Demand_NA / sum_Mult_Demand_NA
            except:
                solution.Demand_NA = 0
            solution.Sales_NA = min([solution.Demand_NA, float(solution.NAFactory)])

            try:
                solution.Demand_Europa = int(self.Game.sizeEurope) * solution.mult_Demand_Europa / sum_Mult_Demand_Europe
            except:
                solution.Demand_Europa = 0
            solution.Sales_Europa =min([solution.Demand_Europa, float(solution.EuropeFactory)])

            try:
                solution.Demand_Asia = int(self.Game.sizeAsia) * solution.mult_Demand_Asia / sum_Mult_Demand_Asia
            except:
                solution.Demand_Asia = 0

            solution.Sales_Asia = min([solution.Demand_Asia, float(solution.AsiaFactory)])

            solution.Sales = solution.Sales_NA + solution.Sales_Asia + solution.Sales_Europa
            solution.Profit = (solution.cost-solution.Prime_cost)*solution.Salesc - (float(solution.Budget))

















