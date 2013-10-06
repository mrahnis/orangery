import orangery as o

file1 = 'data/file_2004.csv'
file2 = 'data/file_2010.csv'
analysis_json = 'analysis.json'
format_json = 'format.json'

# load the configuration
analysis = o.Configuration(analysis_json)
format = o.Configuration(format_json)

# load the survey data
s1 = o.Survey(file1, format.data)
s2 = o.Survey(file2, format.data)

s1.plot()

# select a group of points, in this case a cross section
group = analysis.data['plot']['name']

xs1 = o.group(s1.data, s1.chains, group)
xs2 = o.group(s2.data, s2.chains, group)

# get the endpoints of the group
p1, p2 = o.endpoints(xs1, analysis.data['sections'][0]['reverse'])

# get the benchmarks for a file
# print o.benchmarks(s2.data, s2.chains, format.data)

# make the sections
xs2004 = o.Section(xs1, p1, p2, analysis.data['sections'][0])
xs2010 = o.Section(xs2, p1, p2, analysis.data['sections'][1])

# calculate the change
chg = o.Change(xs2004, xs2010, analysis.data)

chg.plot()
chg.segment()
# chg.save()