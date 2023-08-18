from pylsl import StreamInlet, resolve_stream
import numpy as np

class LSL():
    def __init__(self) -> None:
        self.info = {} #LSL 연결 관련 정보

    def connect(self) -> None:
        """LSL 연결 시도"""
        print()
        while True:
            stream = resolve_stream()
            try:
                info = stream[0]
                self.inlet = StreamInlet(info)
                self.info["samplingRate"] = info.nominal_srate()
                self.info["type"] = info.type()
                self.info["channelNum"] = info.channel_count()
                print("\rconnected")
                break
            except:
                print("\rfinding connection...", end="")
        return

    def receiveData(self) -> tuple[list, float]:
        """LSL에서 데이터 수신"""
        try:
            return self.inlet.pull_sample()
        except:
            self.connect()
            return self.inlet.pull_sample()
        
    def timeCorrection(self) -> float:
        """시간 오차 반환"""
        return self.inlet.time_correction()
    
    def sleep(self, t:float) -> None:
        """t ms 동안 데이터를 받지 않음"""
        deltaTime = 0
        _, prevTime = self.receiveData()
        prevTime*=1000
        while deltaTime <= t:
            _, currTime = self.receiveData()
            currTime*=1000
            deltaTime += currTime - prevTime
            prevTime = currTime
        return
    
    def collectDataByTime(self, t:float) -> tuple[list[list], float]:
        """0~t ms 까지의 데이터"""
        deltaTime = 0   
        # print(deltaTime)
        data, prevTime = self.receiveData()
        prevTime*=1000
        dataTrial = [data]
        mean_dt = 1000/self.info["samplingRate"]
        while deltaTime + mean_dt <= t:
            print(deltaTime)
            data, currTime = self.receiveData()
            currTime*=1000
            deltaTime += currTime - prevTime
            dataTrial.append(data)
            prevTime = currTime
            
        return (dataTrial, deltaTime)
    
def fft(signal:list, t:float) -> tuple[list]:
        """==input==
        signal : Channel * Sample
        t: total time (sec)

        ==output==
        """
        s_fft = np.fft.fft(signal) # 추후 IFFT를 위해 abs를 취하지 않은 값을 저장한다.
        amplitude = abs(s_fft)*(2/len(s_fft)) # 2/len(s)을 곱해줘서 원래의 amp를 구한다.amplitude = abs(s_fft)*(2/len(s_fft)) # 2/len(s)을 곱해줘서 원래의 amp를 구한다.
        frequency = np.fft.fftfreq(len(s_fft), t)
        
        return (amplitude, frequency)