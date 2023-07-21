class Metric(object):
    def __init__(self, name, site, mode=None, query=None, availability_zone=None, aggregates=None, memory=None, product_name=None):
        self.name = name
        self.site = site
        self.mode = mode
        self.query = query
        self.availability_zone = availability_zone
        self.aggregates = aggregates
        self.memory = memory
        self.product_name = product_name
        # print(f"Initializing metric {name} with query: {query} \n")

    def toCSV(self, mytime, myvalue, metric_name, *args):
        features = [mytime, myvalue, metric_name, self.site, self.mode, self.availability_zone, self.aggregates, self.memory, self.product_name]
        features = [f for f in features if f is not None]
        return features + list(args)

class MetricTrigramme(Metric):
    def __init__(self, name, site, trigramme, mode=None, query=None, availability_zone=None, aggregates=None, memory=None, product_name=None):
        super(MetricTrigramme, self).__init__(name, site, mode, query, availability_zone, aggregates, memory, product_name)
        self.trigramme = trigramme

    def toCSV(self, mytime, myvalue, metric_name, *args):
        features = [mytime, myvalue, metric_name, self.site, self.mode, self.availability_zone, self.aggregates, self.memory, self.product_name, self.trigramme]
        features = [f for f in features if f is not None]
        return features + list(args)


class MetricServer(Metric):
    def __init__(self, name, site, trigramme, num_server, mode=None, query=None, availability_zone=None, aggregates=None, memory=None, product_name=None):
        super(MetricServer, self).__init__(name, site, mode, query, availability_zone, aggregates, memory, product_name)
        self.trigramme = trigramme
        self.num_server = num_server

    def toCSV(self, mytime, myvalue, metric_name, *args):
        features = [mytime, myvalue, metric_name, self.site, self.mode, self.availability_zone, self.aggregates, self.memory, self.product_name, self.trigramme, self.num_server]
        features = [f for f in features if f is not None]
        return features + list(args)


class MetricGlobale(Metric):
    def __init__(self, name, site, mode=None, query=None, availability_zone=None, aggregates=None, memory=None, product_name=None):
        super(MetricGlobale, self).__init__(name, site, mode, query, availability_zone, aggregates, memory, product_name)

    def toCSV(self, mytime, myvalue, metric_name, *args):
        features = [mytime, myvalue, metric_name, self.site, self.mode, self.availability_zone, self.aggregates, self.memory, self.product_name]
        features = [f for f in features if f is not None]
        return features + list(args)


