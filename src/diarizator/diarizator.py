from pyannote.audio import Pipeline
import torch

from config.config import DIARIZATION_ACCESS_TOKEN, CUDA

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.0",
    use_auth_token=DIARIZATION_ACCESS_TOKEN)

if CUDA:
    pipeline.to(torch.device("cuda"))

class Diarizator():
    def __init__(self, filepath):
        self.diarization = pipeline(filepath)

    def render(self):
        self.final_pred = self.prepare_segments()
        return self.final_pred
    
    def prepare_segments(self):
        """
        объединяет предыдущие функции
    
        :diarization:  результат работы pipeline
        """
        pred = list(self.diarization.itertracks(yield_label=True))
        listed_pred = [self.segment_to_list(pr) for pr in pred]
        grouped_pred = self.group_speakers(listed_pred)
        fixed_pred = self.remove_short_segs(grouped_pred, 0.5)
        final_pred = self.cut_segments(fixed_pred)
    
        return final_pred
    
    @staticmethod
    def segment_to_list(arr):
        return (list(arr[0]), arr[2])

    @staticmethod
    def group_speakers(segs):
        """
        объединяет последовательные интервалы с одинаковым speaker 
    
        :segs: list, [[start, stop], speaker],
        *start*, *stop* - time interval in seconds, float
        *speaker* - speaker name, str
        """
        grouped = []
        last_l = segs[0][0][0]
        last_speaker = segs[0][1]

        for segment in segs:
            if segment[1] != last_speaker:
                grouped.append([[last_l, segment[0][1]], last_speaker])
                last_l = segment[0][0]
                last_speaker = segment[1]

        # add last segment
        idx = len(segs) - 1
        grouped.append([[last_l, segs[idx][0][1]], last_speaker])
    
        return grouped

    @staticmethod
    def remove_short_segs(segs, threshold=0.5):
        """
        удаляет слишком интервалы, меньшие порога
    
        :threshold: - пороговое значение, в секундах
        """
        output = []
        last_l = segs[0][0][0]
        last_speaker = segs[0][1]

        for segment in segs:
            lborder = segment[0][0]
            rborder = segment[0][1]

            if (rborder - lborder) > threshold:
                if segment[1] != last_speaker:
                    output.append([[last_l, rborder], last_speaker])
                    last_l = lborder
                    last_speaker = segment[1]

        # add last segment
        idx = len(segs) - 1
        lborder = segs[idx][0][0]
        rborder = segs[idx][0][1]

        if (rborder - lborder) > threshold:
            output.append([[last_l, segs[idx][0][1]], last_speaker])
        
        return output

    @staticmethod
    def cut_segments(segs):
        """
        переопределяет конец сегмента, который накладывается на следующий сегмент
        """
        fixed_segs = []
        last_l = segs[0][0][0]

        for i, segment in enumerate(segs):
            if i == (len(segs) - 1):
                fixed_segs.append(segment)
                break
            else:
                fixed_segs.append(segment)
                fixed_segs[i][0][1] = min(segment[0][1], segs[i+1][0][0])
            
        return fixed_segs