class Metric(object):
        def __init__(self, name, site, query):
            self.name = name
            self.site = site
            self.query = query
            


class MetricTrigramme(Metric):
    def __init__(self, name, site, query, trigramme):
            super(MetricTrigramme, self).__init__(name, site, query)
            self.trigramme = trigramme

    def toCSV(self, mytime, myvalue, metric_name, site):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            return m_result
        

class MetricServer(Metric):
    def __init__(self, name, site, query, trigramme, num_server):
            super(MetricServer, self).__init__(name, site, query)
            self.trigramme = trigramme
            self.num_server = num_server

    def toCSV(self, mytime, myvalue, metric_name, site):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            return m_result


class MetricGlobale(Metric):
    def __init__(self, name, site, query):
            super(MetricGlobale, self).__init__(name, site, query)

    def toCSV(self, mytime, myvalue, metric_name, site):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            return m_result
