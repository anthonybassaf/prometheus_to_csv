class Metric(object):
        def __init__(self, name, site, mode, query):
            self.name = name
            self.site = site
            self.mode = mode
            self.query = query
            


class MetricTrigramme(Metric):
    def __init__(self, name, site, mode, query, trigramme):
            super(MetricTrigramme, self).__init__(name, site, mode, query)
            self.trigramme = trigramme


    def toCSV(self, mytime, myvalue, metric_name, site, mode):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(mode)
            return m_result
        

class MetricServer(Metric):
    def __init__(self, name, site, mode, query, trigramme, num_server):
            super(MetricServer, self).__init__(name, site, mode, query)
            self.trigramme = trigramme
            self.num_server = num_server

    def toCSV(self, mytime, myvalue, metric_name, site, mode):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(mode)
            return m_result


class MetricGlobale(Metric):
    def __init__(self, name, site, mode, query):
            super(MetricGlobale, self).__init__(name, site, mode, query)

    def toCSV(self, mytime, myvalue, metric_name, site, mode):
            m_result = []
            m_result.append(mytime)
            m_result.append(myvalue)
            m_result.append(metric_name)
            m_result.append(site)
            m_result.append(mode)
            return m_result
