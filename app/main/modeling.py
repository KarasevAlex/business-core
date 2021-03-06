from ..database import Solutions, Games, Period
from .. import db
import  random
class Modeling():
    Game = None
    Current_period_solution = None
    Current_period_solutions = None
    Previous_solutions = None
    Current_period = None

    def generateGame(self, current_user, form):
        self.Current_period = form['period']
        self.Game = Games.query.filter_by(id=current_user.game_id).first()
        self.Previous_solutions = Solutions.query.filter_by()
        self.Current_period_solutions = Solutions.query.filter_by(period_id=form['period']).all()
        if len(self.Current_period_solutions) == 0:
            Sol = Solutions.getPreviousSolutions(self.Current_period)
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
                    self.Current_period_solution = previous_solution
        self.generateResult()

    def adminRecount(self, period_id, game):
        self.Current_period = period_id
        self.Game = game
        self.Previous_solutions = Solutions.query.filter_by()
        self.Current_period_solutions = Solutions.query.filter_by(period_id=period_id).all()
        self.generateResult()

    def generateDemo(self, solution, game):
        self.Current_period_solution = solution
        self.Game = game
        botSolution = self.generateBotSolution()
        botSolution.count_personal_params(game, isDemo=True)
        self.Current_period_solutions = []
        self.Current_period_solutions.append(self.Current_period_solution)
        self.Current_period_solutions.append(botSolution)
        self.generateResult(isDemo=True)

    def getPeriod(self):
        return Period.query.filter_by(id=self.Current_period).first()

    def getGame(self):
        return self.Game

    def getCurrentSolution(self):
        return self.Current_period_solution

    def getCurrentSolutions(self):
        return self.Current_period_solutions

    def resultDemo(self):
        pass

    def generateBotSolution(self):
        solutions = Solutions()
        solutions.cost = random.randint(3, 10)
        solutions.niokrSS = random.randint(10, 30)
        solutions.niokrQuality = random.randint(20, 40) - solutions.niokrSS
        if solutions.niokrQuality < 0:
            solutions.niokrQuality = 0
        solutions.NAFactory = random.randint(30, 50)
        solutions.NAPromotion = 100 - solutions.NAFactory - (solutions.NAFactory*(0.2)) - solutions.niokrSS - solutions.niokrQuality
        solutions.Budget = 100
        return solutions

    def generateResult(self, isDemo=False):

        sum_Mult_Demand_NA = 0
        sum_Mult_Demand_Asia = 0
        sum_Mult_Demand_Europe = 0

        if not isDemo:
            profit_acc = 0
            for solution in self.Current_period_solutions:
                sum_Mult_Demand_NA += solution.mult_Demand_NA
                sum_Mult_Demand_Asia += solution.mult_Demand_Asia
                sum_Mult_Demand_Europe += solution.mult_Demand_Europa
            for solution in self.Current_period_solutions:
                try:
                    solution.Demand_NA = round(int(self.Game.sizeNA) * solution.mult_Demand_NA / sum_Mult_Demand_NA)
                except:
                    solution.Demand_NA = 0
                solution.Sales_NA = min([solution.Demand_NA, float(solution.NAFactory)])

                try:
                    solution.Demand_Europa = round(int(self.Game.sizeEurope) * solution.mult_Demand_Europa / sum_Mult_Demand_Europe)
                except:
                    solution.Demand_Europa = 0
                solution.Sales_Europa = min([solution.Demand_Europa, float(solution.EuropeFactory)])

                try:
                    solution.Demand_Asia = round(int(self.Game.sizeAsia) * solution.mult_Demand_Asia / sum_Mult_Demand_Asia)
                except:
                    solution.Demand_Asia = 0

                solution.Sales_Asia = min([solution.Demand_Asia, float(solution.AsiaFactory)])

                solution.Sales = solution.Sales_NA + solution.Sales_Asia + solution.Sales_Europa

                if solution.Budget is not None:
                    solution.Profit = ((float(solution.cost)) - (float(solution.Prime_cost))) * (
                    float(solution.Sales)) - (float(solution.Budget))
                    solution.Acc_Profit = Solutions.getAccProfit(solution.gamer_id)

                else:
                    solution.Profit = 0

        else:
            for solution in self.Current_period_solutions:
                sum_Mult_Demand_NA += solution.mult_Demand_NA

            for solution in self.Current_period_solutions:
                try:
                    solution.Demand_NA = round(int(self.Game.sizeNA) * solution.mult_Demand_NA / sum_Mult_Demand_NA)
                except:
                    solution.Demand_NA = 0
                solution.Sales_NA = min([solution.Demand_NA, float(solution.NAFactory)])

                solution.Sales = solution.Sales_NA

                if solution.Budget is not None:
                    solution.Profit = ((float(solution.cost)) - (float(solution.Prime_cost))) * (
                    float(solution.Sales)) - (float(solution.Budget))
                else:
                    solution.Profit = 0
















