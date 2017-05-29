import yaml
import datetime
import matplotlib.pyplot as plt


class TimelinePlotter(object):
    def __init__(self):
        self.events = {}

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
        plt.figure(figsize=(16, self.get_max('pos') * 3))
        for i in self.events.keys():
            p = plt.plot([self.events[i]['start'], self.events[i]['end']],
                         [self.events[i]['pos'], self.events[i]['pos']],
                         marker='o', lw=4)
            role_text = self.events[i]['task'] + "\n@ " + self.events[i]['place']
            if self.events[i]['type'] == "Professional":
                plt.text(self.events[i]['start'], self.events[i]['pos'] + 0.05, role_text,
                         ha='left', va='bottom', rotation=45, size=7, color=p[0].get_color())
                plt.text(self.events[i]['start'], self.events[i]['pos'] - 0.05, str(self.events[i]['start']),
                         ha='left', va='top', size=6, rotation=0, color=p[0].get_color())
            else:
                plt.text(self.events[i]['start'], self.events[i]['pos'] - 0.05, role_text,
                         ha='left', va='top', rotation=-45, size=7, color=p[0].get_color())
                plt.text(self.events[i]['start'], self.events[i]['pos'] + 0.05, str(self.events[i]['start']),
                         ha='left', va='bottom', size=6, rotation=0, color=p[0].get_color())
            self.events[i]['color'] = p[0].get_color()
        plt.ylim(self.get_min('pos') - 2, self.get_max('pos') + 2)
        plt.xlim(self.get_min('start') - datetime.timedelta(days=150),
                 self.get_max('end') + datetime.timedelta(days=500))
        plt.show()

    def assign_positions(self):
        past_events = []
        for i in self.events.keys():
            overlaps = self.overlaps(i, past_events)
            print(i)
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
