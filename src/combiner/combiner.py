class Combiner():
    def __init__(self, diarization, text_with_time):
        self.diar = diarization
        self.text = text_with_time
        self.dict = {}

    def combine(self):
        self.prepare_dict()
        final_text = self.prepare_text()
        return final_text

    def prepare_dict(self):
        for text_seg, text in self.text:
            #start = self.format_time(text_seg[0])  # added
            #stop = self.format_time(text_seg[1])  # added
            #text = f'{start} - {stop}: '  # added
            #text += '\n'  # added
            max_cross = 0
            argmax = 0
            for i, [diar_seg, _] in enumerate(self.diar):
                cross = self.intersection(text_seg, diar_seg)
                if cross > max_cross:
                    max_cross = cross
                    argmax = i
            try:
                self.dict[argmax] += text
            except:
                self.dict[argmax] = text
        return self.dict

    def prepare_text(self):
        final_text = []
        for i in range(len(self.diar)):
            [start, stop], speaker = self.diar[i]
            if i in self.dict.keys():
                start_time = self.format_time(start)
                stop_time = self.format_time(stop)
                final_text.append([self.dict[i], speaker])
        return final_text

    def intersection(self, seg1, seg2):
        rborder = min(seg1[1], seg2[1])
        lborder = max(seg1[0], seg2[0])
        ans = rborder - lborder

        if ans <= 0:
            return 0
        else:
            return ans

    def convert_time(self, tm):
        int_tm = int(tm)

        return int_tm // 3600, int_tm % 3600 // 60, int_tm % 60

    def format_time(self, tm):
        hours, mins, secs = self.convert_time(tm)
        ans = ''

        if hours != 0:
            ans += str(hours) + ":"
        if mins // 10 == 0:
            ans += "0"
        ans += str(mins) + ":"
        if secs // 10 == 0:
            ans += "0"
        ans += str(secs)

        return ans