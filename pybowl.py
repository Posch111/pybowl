import random

LAST_FRAME_INDEX = 9
PINS_PER_LANE = 10

class Bowler:
    """A player in the bowling game"""
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.frame_set = FrameSet()
        self.current_frame = None # the frame for which the Bowler is throwing
    
    @property
    def done_bowling(self):
        return self.frame_set.complete

    @property
    def score(self):
        return self.frame_set.score

    def bowl_frame(self, autoplay=False):
        if self.current_frame == None:
            # first frame of the round
            self.current_frame = self.frame_set.frames[0]
        else:
            self.current_frame = self.current_frame.next_frame

        frame = self.current_frame
        if frame.index != LAST_FRAME_INDEX:
            print(f"{self.name}, bowl frame {frame.index + 1}.")
        else:
            print(f"{self.name}, this bowl your final frame {frame.index + 1}.")
        
        frame.shot1 = self.roll_ball(pins_remaining=PINS_PER_LANE, autoplay=autoplay)

        if not frame.done:
            if frame.shot1_strike:
                if frame.index == LAST_FRAME_INDEX:
                    print(f"Strike! You get two more rolls.")
                else:
                    print(f"You bowled a strike! Frame over.")
            else:
                print(f"You hit {frame.shot1} pin(s). {str(frame.pins_remaining)} pins standing, roll again.")
            frame.shot2 = self.roll_ball(pins_remaining=(PINS_PER_LANE - frame.shot1), autoplay=autoplay)
        
        if not frame.done:
            if frame.shot2_strike:
                print(f"Another strike! Bowl your final roll.")
            elif frame.spare:
                if frame.index == LAST_FRAME_INDEX:
                    print(f"Spare! Bowl your final roll.")
                else:
                    print(f"You bowled a Spare! Frame over.")
            elif frame.index == LAST_FRAME_INDEX:
                print(f"You hit {frame.shot2} pin(s). You have finished your round.")
            else:
                print(f"You hit {frame.shot2} pin(s). Frame over.")

        if not frame.done:
            print(f"You hit {frame.shot2} pin(s). Roll again.")
            frame.shot3 = self.roll_ball(pins_remaining=(PINS_PER_LANE - frame.shot1), autoplay=autoplay)
            if frame.shot3_strike:
                print(f"You hit a strike for your final roll! You have finished your round.")
            else:
                print(f"You hit {frame.shot3} pin(s) for your final roll. You have finished your round.")

    def roll_ball(self, pins_remaining, autoplay=False):
        if autoplay:
            pins_knocked = random.randint(0, pins_remaining)
        else:
            roll_complete = False
            while not roll_complete:
                try:
                    pins_knocked = int(input())
                except ValueError as e:
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
        self.frames = [self.Frame(i) for i in range(LAST_FRAME_INDEX+1)]
        
        for frame in self.frames[:-1]:
            frame.next_frame = self.frames[frame.index+1]

    # indicates all 10 frames of the FrameSet has been completed
    @property
    def complete(self):
        return  (False not in [f.done for f in self.frames])
    
    @property
    def score(self):
        total_score = sum([f.score for f in self.frames])
    
    def __str__(self):
        s =  '|Frames:                        '
        s =  '|_____________________________\n'
        for i in range(len(self.frames)):
            s += '|'
            s += f' {i}  '
            s += '|'
        for f in self.frames:
            s += '|'
            s += f' {f.score} '
            s += '|'
        s += '______________________________\n'
        s += 'total: ' + str(self.score)
        return s

    class Frame:
        """A single frame of a FrameSet."""
        def __init__(self, index):
            self.index = index
            self.next_frame = None
            self._scoring_complete = False
            self._done = False
            self._score = 0
            self._shot1 = None
            self._shot2 = None
            self._shot3 = None
            # total pins hit during the frame
            self._pin_total = 0
            # each shot has a strike indicator to distinguish 
            # between multiple strikes in the final frame.
            self.shot1_strike = False
            self.shot2_strike = False
            self.shot3_strike = False
            self.spare = False
            # the number of pins remaining, which can be reset up to two times on the final frame.
            self._pins_remaining
        
        # Indicates True if all rolls have been done for the frame.
        @property
        def done(self):
            return self._done

        @property
        def pin_total(self):
            pins = 0
            if self._shot1:
                pins += self._shot1
            if self._shot2:
                pins += self._shot2
            if self._shot3:
                pins += self._shot3
            return pins
        
        @property
        def pins_remaining(self):
            return self._pins_remaining
        
        # The current score for the frame.
        # It can be partially calculated before the frame is done.
        @property
        def score(self):
            if self._scoring_complete:
                return self._score
            elif self._done:
                _scoring_complete = True
            
            frame_score = 0
            if self.index == LAST_FRAME_INDEX:
                return self.pin_total
            elif self.shot1_strike:
                frame_score += PINS_PER_LANE
                if self.next_frame.strike:
                    
                elif self.next_frame.strike:
                    frame_score += self.next_frame.score
                    third_shot = self.next_frame.next_frame.shot1
                    if third_shot:
                        frame_score += third_shot
                        self._scoring_complete = True
                else:
                    frame_score += self.next_frame.score
            elif self.spare:
                frame_score += PINS_PER_LANE + self.next_frame.shot1
            else:
                frame_score = self.pin_total
            
            self._score = frame_score
            return frame_score

        @property
        def shot1(self):
            return self._shot1

        @shot1.setter
        def shot1(self, pins):
            if self._done:
                raise ValueError("Frame is somehow already finished before the 1st shot: " + str(self))
            elif pins > PINS_PER_LANE or pins < 0:
                raise ValueError("Invalid number of pins after shot 2 for " + str(self))
            
            self._shot1 = pins
            self._pin_total += pins
            if pins == PINS_PER_LANE:
                self.strike = True
                self._done == True
                if self.index == LAST_FRAME_INDEX:
                    # the last frame resets the pin count after a strike on shot1
                    self._pins_remaining = PINS_PER_LANE
                else:
                    self._pins_remaining = PINS_PER_LANE - pins
            else:
                self._pins_remaining = PINS_PER_LANE - pins
        
        @property
        def shot2(self):
            return self._shot2

        @shot2.setter
        def shot2(self, pins):
            if self.done:
                raise ValueError("Cannot set a value for shot2, frame is finished.\n" + str(self))
            elif (self._shot1 + pins) > PINS_PER_LANE or (self._shot1 + pins) < 0:
                raise ValueError("Invalid number of pins after shot 2 for " + str(self))
            
            self._shot2 = pins
            self._pin_total += pins

            if (self._shot1 + self._shot2) == PINS_PER_LANE:
                self.spare = True 
                # only the last frame has a third shot when all pins are knocked
                if self.index != LAST_FRAME_INDEX:
                    self._done = True
                    self._pins_remaining = 0
                else:
                    self._pins_remaining = PINS_PER_LANE
            else:
                self._pins_remaining = self.PINS_PER_LANE - pins

        @property
        def shot3(self, pins):
            return self._shot3

        @shot3.setter
        def shot3(self, pins):
            if self.index != LAST_FRAME_INDEX:
                raise IndexError(f"Frame has only two shots\n" + str(self))
            elif self.frame_complete:
                raise ValueError("Third shot is not allowed without a strike or spare\n" + str(self))
            elif pins > PINS_PER_LANE or pins < 0:
                raise ValueError("Invalid number of pins for " + str(self))
            else:
                _shot3 = pins
                self.done = True
                self._pins_remaining = self.PINS_PER_LANE - pins
        
        def __str__(self):
            return f"Frame{self.index}(shot1={self.shot1}, shot2={self.shot2}, scoring_complete={self._scoring_complete}, score={self.score})"

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
        
        print('-----------------------------------------------------')
        print('Final Scores:')
        for p in self.bowlers:
            print(f"{p.name}: {str(p.frame_set)}")
            print('-----------------------------------------------------')
