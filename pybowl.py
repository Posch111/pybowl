import random

class Bowler:
    """A player in the bowling game"""
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.frame_set = FrameSet()
        self.frame_index = 0 # the frame for which the Bowler will throw
    
    @property
    def done_bowling(self):
        return self.frame_set.complete

    @property
    def score(self):
        return self.frame_set.score

    def bowl_frame(self, autoplay=False):
        print(f"{self.name}, bowl frame {self.frame_index}.")
        current_frame = self.frame_set.frames[self.frame_index]

        current_frame.shot1 = self.roll_ball(pins_remaining=10,autoplay=autoplay)
        print(current_frame.shot1)
        if current_frame.shot1 != 10:
            print(f"You hit {current_frame.shot1} pins. Roll again.")
            current_frame.shot2 = self.roll_ball(pins_remaining=(10-current_frame.shot1), autoplay=autoplay)
        
        # total_pins = 11
        total_pins = current_frame.shot1 + current_frame.shot2
        if total_pins < 0 or total_pins > 10 :
            raise ValueError(f"Invalid number of total pins knocked in frame: {total_pins}"
                            "shot1_pins: {shot1_pins}, shot2_pins: {shot2_pins}")

        bowl_phrase = ''
        if current_frame.strike:
            bowl_phrase = 'a strike.'
        elif current_frame.spare:
            bowl_phrase = 'a spare.'
        else:
            bowl_phrase = f"a total of {total_pins} pins this round."

        print(f"{self.name} bowled {bowl_phrase}")
        self.frame_index += 1

    def roll_ball(self, pins_remaining, autoplay=False):
        if autoplay:
            pins_knocked = random.randint(0,pins_remaining)
        else:
            roll_complete = False
            while not roll_complete:
                try:
                    pins_knocked = int(input())
                except:
                    print("Enter an integer only")
                    continue

                if pins_knocked > pins_remaining:
                    print(f"No stealing. You only have {pins_remaining} pins standing. Try again")
                elif pins_knocked < 0:
                    print(f"No throwing the ball. Try again")
                else:
                    if pins_knocked == 0:
                        print(f"Gutter ball.")
                    return pins_knocked

class FrameSet:
    "A set of 10 frames to track the score of a single Bowler."
    def __init__(self):
        self.frames = [self.Frame(i) for i in range(10)]

    # indicates all 10 frames of the FrameSet has been completed
    @property
    def complete(self):
        return  (False not in [f.scoring_complete for f in self.frames])
    
    @property
    def score(self):
        total_score = 0
        # for i in range(len(self.frames)):
        #     if not self.frames[i].scoring_complete:
        #         try:
        #             second_frame = 
        #         except:
                    
        #     total_score += f.score

    class Frame:
        """A single frame of a FrameSet."""
        def __init__(self, index):
            print('I am frame', index)
            self.index = index
            self.scoring_complete = False
            self.score = None
            self._shot1 = None
            self._shot2 = None
            self._shot3 = None
            self.strike = False
            self.spare = False

        @property
        def shot1(self):
            return self._shot1

        @shot1.setter
        def shot1(self, pins):
            if pins == 10:
                self.strike = True
            self._shot1 = pins
        
        @property
        def shot2(self):
            return self._shot2

        @shot2.setter
        def shot2(self, pins):
            if self.strike:
                raise ValueError("Cannot set a value for shot2 when this frame is a strike.\n" + self.__str__())
            elif (self._shot1 + pins) > 10 or (self._shot1 + pins) < 0:
                raise ValueError("Invalid number of pins for " + self.__str__())
            
            self._shot2 = pins
            if (self._shot1 + pins) == 10:
                self.spare = True

        @property
        def shot3(self, pins):
            if self.index != 9:
                raise IndexError(f"Frame has only two shots\n" + self.__str__())
            else:
                if (self.strike or self.spare) < 10:
                    raise ValueError("Third shot is not allowed without a strike or spare\n" + self.__str__())
                elif pins > 10 or pins < 0:
                    raise ValueError("Invalid number of pins for " + self.__str__())
                else:
                    _shot3 = pins
        
        def __str__(self):
            s = f"Frame{self.index}(shot1={self.shot1}, shot2={self.shot2}, scoring_complete={self.scoring_complete}, score={self.score}"

class BowlingGame:
    def __init__(self, bowlers, autoplay = False):
        ids = set([b.id for b in bowlers])
        if len(ids) != len(bowlers):
            raise AttributeError("Two Bowlers cannot have the same id.")
        
        self.bowlers = bowlers
        self.autoplay = autoplay
        self.frame = 0

    def start(self):
        print('Starting game...')
        print('On your turn, roll (enter a number from 0 to 10) to knock down pins') 

        while False in [p.done_bowling for p in self.bowlers]:
            for p in self.bowlers:
                p.bowl_frame()
                
    
    # def bowl_player(self, player):
