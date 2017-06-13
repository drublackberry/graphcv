from graphcv import TimelinePlotter
import os

tl = TimelinePlotter("Andreu Mora")
tl.load_events(os.path.join(os.environ['PROJECT_ROOT'], 'data', 'in', 'events.yml'))
tl.plot()
