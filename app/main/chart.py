from flask import render_template
class Chart:
    solutions= None
    users = None
    labels = []
    costSS_dataset = []
    quality_chart_dataset = {}
    demand_chart_dataset = []
    factories_chart_dataset = []
    sales_chart_dataset = []
    profit_chart_dataset = {}
    promotion_chart_dataset = []
    def __init__(self, solution, users):
        self.solutions = solution
        self.users = users
        for user in self.users:
            self.labels.append(user.name)

        self.setData()

    def setData(self):
        # Цены СС
        cost = {}
        cost['label'] = 'Цена'
        cost['data'] = []
        cost['fillColor'] = "rgba(31, 58, 147, 1)"
        costSS = {}
        costSS['label'] = 'Себестоимость'
        costSS['data'] = []
        costSS['fillColor'] = "rgba(94, 102, 255, 1)"
        # Качество

        self.quality_chart_dataset['label'] = "Качество"
        self.quality_chart_dataset['data'] = []
        self.quality_chart_dataset['fillColor'] = "rgba(31, 58, 147, 1)"
        # Спрос

        demand_NA = {}
        demand_NA['label'] = 'Северная Америка'
        demand_NA['data'] = []
        demand_NA['fillColor'] = "rgba(150, 40, 27, 1)"
        demand_Europe = {}
        demand_Europe['label'] = 'Европа'
        demand_Europe['data'] = []
        demand_Europe['fillColor'] = "rgba(65, 131, 215, 1)"
        demand_Asia = {}
        demand_Asia['label'] = 'Азия'
        demand_Asia['data'] = []
        demand_Asia['fillColor'] = "rgba(242, 121, 53, 1)"
        # Заводы
        NAFactory = {}
        NAFactory['label'] = 'Северная Америка'
        NAFactory['data'] = []
        NAFactory['fillColor'] = "rgba(150, 40, 27, 1)"
        EuropeFactory = {}
        EuropeFactory['label'] = 'Европа'
        EuropeFactory['data'] = []
        EuropeFactory['fillColor'] = "rgba(65, 131, 215, 1)"
        AsiaFactory = {}
        AsiaFactory['label'] = 'Азия'
        AsiaFactory['data'] = []
        AsiaFactory['fillColor'] = "rgba(242, 121, 53, 1)"
        # Продажи
        Sales_NA = {}
        Sales_NA['label'] = 'Северная Америка'
        Sales_NA['data'] = []
        Sales_NA['fillColor'] = "rgba(150, 40, 27, 1)"
        Sales_Europa = {}
        Sales_Europa['label'] = 'Европа'
        Sales_Europa['data'] = []
        Sales_Europa['fillColor'] = "rgba(65, 131, 215, 1)"
        Sales_Asia = {}
        Sales_Asia['label'] = 'Азия'
        Sales_Asia['data'] = []
        Sales_Asia['fillColor'] = "rgba(242, 121, 53, 1)"
        Sales = {}
        Sales['label'] = 'Cумма'
        Sales['data'] = []
        Sales['fillColor'] = "rgba(63, 195, 128, 1)"
        # Прибыль
        self.profit_chart_dataset['label'] = "Прибыль"
        self.profit_chart_dataset['data'] = []
        self.profit_chart_dataset['fillColor'] = "rgba(65, 131, 215, 1)"
        # Продвижение

        NAPromotion = {}
        NAPromotion['label'] = 'Северная Америка'
        NAPromotion['data'] = []
        NAPromotion['fillColor'] = "rgba(150, 40, 27, 1)"
        EuropePromotion = {}
        EuropePromotion['label'] = 'Европа'
        EuropePromotion['data'] = []
        EuropePromotion['fillColor'] = "rgba(65, 131, 215, 1)"
        AsiaPromotion = {}
        AsiaPromotion['label'] = 'Азия'
        AsiaPromotion['data'] = []
        AsiaPromotion['fillColor'] = "rgba(242, 121, 53, 1)"

        for solution in self.solutions:
            cost['data'].append(solution.cost)
            costSS['data'].append(solution.Prime_cost)
            self.quality_chart_dataset['data'].append(solution.mult_Quality)
            self.profit_chart_dataset['data'].append(solution.Profit)
            demand_NA['data'].append(solution.Demand_NA)
            demand_Europe['data'].append(solution.Demand_Europa)
            demand_Asia['data'].append(solution.Demand_Asia)

            NAFactory['data'].append(solution.NAFactory)
            EuropeFactory['data'].append(solution.EuropeFactory)
            AsiaFactory['data'].append(solution.AsiaFactory)
            Sales_NA['data'].append(solution.Sales_NA)
            Sales_Europa['data'].append(solution.Sales_Europa)
            Sales_Asia['data'].append(solution.Sales_Asia)
            Sales['data'].append(solution.Sales)

            AsiaPromotion['data'].append(solution.AsiaPromotion)
            EuropePromotion['data'].append(solution.EuropePromotion)
            NAPromotion['data'].append(solution.NAPromotion)

        self.costSS_dataset.append(cost)
        self.costSS_dataset.append(costSS)

        self.demand_chart_dataset.append(demand_NA)
        self.demand_chart_dataset.append(demand_Europe)
        self.demand_chart_dataset.append(demand_Asia)

        self.factories_chart_dataset.append(NAFactory)
        self.factories_chart_dataset.append(EuropeFactory)
        self.factories_chart_dataset.append(AsiaFactory)

        self.sales_chart_dataset.append(Sales_NA)
        self.sales_chart_dataset.append(Sales_Europa)
        self.sales_chart_dataset.append(Sales_Asia)
        self.sales_chart_dataset.append(Sales)

        self.promotion_chart_dataset.append(NAPromotion)
        self.promotion_chart_dataset.append(AsiaPromotion)
        self.promotion_chart_dataset.append(EuropePromotion)

    def render(self):
        return render_template('chart-script.html', labels=self.labels,
                               costSS_dataset=self.costSS_dataset,
                               quality_chart_dataset=self.quality_chart_dataset,
                               demand_chart_dataset=self.demand_chart_dataset,
                               factories_chart_dataset=self.factories_chart_dataset,
                               sales_chart_dataset=self.sales_chart_dataset,
                               profit_chart_dataset=self.profit_chart_dataset,
                               promotion_chart_dataset=self.promotion_chart_dataset)

