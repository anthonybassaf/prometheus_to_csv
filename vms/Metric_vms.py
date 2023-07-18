class Metric(object):
        def __init__(self, name, site, availability_zone, aggregates, query):
            self.name = name
            self.site = site
            self.availability_zone = availability_zone
            self.aggregates = aggregates
            self.query = query
            


class MetricTrigramme(Metric):
    def __init__(self, name, site, availability_zone, aggregates, query, trigramme):
            super(MetricTrigramme, self).__init__(name, site, availability_zone, aggregates, query)
            self.trigramme = trigramme

#     def toCSV(self, mytime, myvalue, metric_name, site, zone, aggregates):
#             return [metric_name, myvalue, site, zone, mytime, aggregates]


    def toCSV(self, mytime, myvalue, metric_name, site, availability_zone, aggregates):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(availability_zone)
            m_result.append(aggregates)   
        #     for m_key in metric_name.keys:
        #             m_result.append(metric_name[m_key], site, availability_zone, aggregates)
            return m_result
        

class MetricServer(Metric):
    def __init__(self, name, site, availability_zone, aggregates, query, trigramme, num_server):
            super(MetricServer, self).__init__(name, site, availability_zone, aggregates, query)
            self.trigramme = trigramme
            self.num_server = num_server

    def toCSV(self, mytime, myvalue, metric_name, site, availability_zone, aggregates):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(availability_zone)
            m_result.append(aggregates)
            return m_result


class MetricGlobale(Metric):
    def __init__(self, name, site, availability_zone, aggregates, query):
            super(MetricGlobale, self).__init__(name, site, availability_zone, aggregates, query)

    def toCSV(self, mytime, myvalue, metric_name, site, availability_zone, aggregates):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(availability_zone)
            m_result.append(aggregates)
            return m_result
