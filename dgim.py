import random
from collections import deque
class DGIM:
    def __init__(self, window_size):
        self.window_size = window_size
        self.buckets = deque()

        
    def update(self, bit):


        if bit == 1:
            self.buckets.append({'size': 1, 'timestamp': 0})
            self.merge_buckets()
            
        for bucket in self.buckets:
            if bucket['timestamp'] <= self.window_size:
                bucket['timestamp'] += 1
        self.drop_buckets()

        

    def merge_buckets(self):
        i = 0
        while i < len(self.buckets) - 2:
            if self.buckets[i]['size'] == self.buckets[i + 2]['size']:
                self.buckets[i]['size'] += self.buckets[i + 1]['size'] # Double the size
                self.buckets[i]['timestamp'] = self.buckets[i + 1]['timestamp']  # Adjust timestamp
                del self.buckets[i + 1]
            else:
                i += 1


    def drop_buckets(self):
        ''' drop buckets when their end-time > window size time units in the past
        '''
        while len(self.buckets) > 0 and self.buckets[0]['timestamp'] > self.window_size:
            del self.buckets[0]
    
    def estimate_count(self):
        total_count = 0
        for bucket in self.buckets:
            total_count += bucket['size']

        return total_count - (self.buckets[0]['size'] // 2)


if __name__ == "__main__":
    stream = [0, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 0]

    dgim = DGIM(12)
    for bit in stream:
        dgim.update(bit)
    print("bucket: ", dgim.buckets)
    print("Estimate count:", dgim.estimate_count())
    print()
    # If the next incoming bit is 0
    dgim.update(0)
    print("bucket: ", dgim.buckets)
    print("Estimate count:", dgim.estimate_count())
    print()
    # If the next incoming bit is 1
    dgim.update(1)
    print("bucket: ", dgim.buckets)
    print("Estimate count:", dgim.estimate_count())
