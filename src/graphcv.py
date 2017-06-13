import yaml
import datetime
import matplotlib.pyplot as plt


class TimelinePlotter(object):
    def __init__(self, name):
        self.events = {}
        self.name = name

    def load_events(self, yml_file):
        stream = open(yml_file, "r")
        for event in yaml.load_all(stream):
            self.events[event['label']] = event
            # convert dates
            for t in ['start', 'end']:
                if event[t] == "present":
                    event[t] = [datetime.date.today().year, datetime.date.today().month, datetime.date.today().day]
                self.events[event['label']][t] = datetime.date(event[t][0], event[t][1], event[t][2])
            self.events[event['label']]['pos'] = - int(self.events[event['label']]['type'] == "Education")
        self.assign_positions()

    def plot(self):
        amp = 2.
        angle = 45.
        plt.figure(figsize=(16, self.get_max('pos') * 3))
        for i in self.events.keys():
            role_text = self.events[i]['task'] + "\n@ " + self.events[i]['place']
            if self.events[i]['type'] == "Professional":
                p = plt.plot([self.events[i]['start'], self.events[i]['end']],
                             [amp * self.events[i]['pos'], amp * self.events[i]['pos']],
                             marker='o', lw=4, linestyle='-')
                plt.text(self.events[i]['start'], amp*self.events[i]['pos'] + 2*0.1, role_text,
                         ha='left', va='bottom', rotation=angle, size=8, color=p[0].get_color())
                plt.text(self.events[i]['start'], amp*self.events[i]['pos'] - 2*0.1, str(self.events[i]['start']),
                         ha='left', va='top', size=6, rotation=0, color=p[0].get_color())
            else:
                p = plt.plot([self.events[i]['start'], self.events[i]['end']],
                             [amp * self.events[i]['pos'], amp * self.events[i]['pos']],
                             marker='o', lw=4, linestyle='--')
                plt.text(self.events[i]['start'], amp*self.events[i]['pos'] - 2*0.1, role_text,
                         ha='left', va='top', rotation=-angle, size=8, color=p[0].get_color())
                plt.text(self.events[i]['start'], amp*self.events[i]['pos'] + 2*0.1, str(self.events[i]['start']),
                         ha='left', va='bottom', size=7, rotation=0, color=p[0].get_color())
            self.events[i]['color'] = p[0].get_color()
        plt.ylim(self.get_min('pos') - amp*4, self.get_max('pos') + amp*4)
        min_date = self.get_min('start') - datetime.timedelta(days=150)
        max_date = self.get_max('end') + datetime.timedelta(days=600)
        plt.xlim(min_date, max_date)
        plt.tick_params(axis='y', left='off', right='off', labelleft='off')
        plt.title('Activity for ' + self.name)
        #plt.text(self.get_min('start'), self.get_max('pos'), '- professional \n -- education',
        #         bbox={'facecolor': 'black', 'alpha': 0.2, 'pad': 10}, fontsize=7)
        plt.axes().xaxis.grid(alpha=0.4, linestyle='--')
        plt.annotate(' education', xy=(max_date, self.get_min('pos') - amp*3), xytext=(max_date, -1*amp),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.annotate(' professional', xy=(max_date, self.get_max('pos') + amp*3), xytext=(max_date, 0*amp),
                     arrowprops=dict(facecolor='black', shrink=0.05))
        plt.plot([min_date, max_date], [-0.5*amp, -0.5*amp], 'k--', alpha=.4)
        plt.show()

    def assign_positions(self):
        past_events = []
        for i in self.events.keys():
            overlaps = self.overlaps(i, past_events)
            if overlaps:
                if self.events[i]['type'] == "Professional":
                    new_pos = min(set(range(len(self.events))) - set(overlaps))
                else:
                    new_pos = max(set(range(-1, -len(self.events), -1)) - set(overlaps))
                self.events[i]['pos'] = new_pos
            past_events.append(i)

    def overlaps(self, label, past_events):
        where = []
        for i in [x for x in past_events if x != label]:
            if (self.events[label]['start'] < self.events[i]['end']) & \
                    (self.events[label]['start'] > self.events[i]['start']) & \
                    (self.events[label]['type'] == self.events[i]['type']):
                where.append(self.events[i]['pos'])
        return where

    def get_max(self, field):
        all_items = [self.events[i][field] for i in self.events.keys()]
        return max(all_items)

    def get_min(self, field):
        all_items = [self.events[i][field] for i in self.events.keys()]
        return min(all_items)
