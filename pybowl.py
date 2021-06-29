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
            print(f"{self.name}, bowl frame {LAST_FRAME_INDEX + 1}, your final frame.")
        
        frame.shot1 = self.roll_ball(pins_remaining=frame.pins_remaining, autoplay=autoplay)

        if frame.shot1_strike:
            if frame.index == LAST_FRAME_INDEX:
                print(f"Strike! You get two more rolls.")
            else:
                print(f"You bowled a strike! Frame over.")
        else:
            print(f"You hit {frame.shot1} pin(s). {str(frame.pins_remaining)} pins standing, roll again.")

        if not frame.done:
            frame.shot2 = self.roll_ball(pins_remaining=frame.pins_remaining, autoplay=autoplay)
            if frame.shot2_strike:
                print(f"Another strike! Bowl your final roll.")
            elif frame.spare:
                if frame.index == LAST_FRAME_INDEX:
                    print(f"Spare! Bowl your final roll.")
                else:
                    print(f"You bowled a Spare! Frame over.")
            elif frame.index == LAST_FRAME_INDEX:
                if frame.done:
                    print(f"You hit {frame.shot2} pin(s). You have finished your round.")
                else:
                    print(f"You hit {frame.shot2} pin(s). Roll again.")
            else:
                print(f"You hit {frame.shot2} pin(s). Frame over.")

        if not frame.done:
            frame.shot3 = self.roll_ball(pins_remaining=frame.pins_remaining, autoplay=autoplay)
            if frame.shot3_strike:
                print(f"You hit a strike for your final roll! You have finished your round.")
            else:
                print(f"You hit {frame.shot3} pin(s) for your final roll. You have finished your round.")

    def roll_ball(self, pins_remaining, autoplay=False):
        if autoplay:
           return random.randint(0, pins_remaining)
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
        return sum([f.score for f in self.frames])
    
    def reset(self):
        self.frames = [self.Frame(i) for i in range(LAST_FRAME_INDEX+1)]
        
        for frame in self.frames[:-1]:
            frame.next_frame = self.frames[frame.index+1]
    
    def __str__(self):
        row_format ="|{:>4}" * (len(self.frames) + 1)
        s = row_format.format("Frame:", *[f.index for f in self.frames])
        s += '\n'
        s += row_format.format("Score:", *[f.score for f in self.frames])
        s += f"\nTotal Score = {self.score}"
        return s

    class Frame:
        """A single frame of a FrameSet."""
        def __init__(self, index):
            self.index = index
            self.next_frame = None
            self._scoring_complete = False
            self._done = False
            self._score = 0
            self._shot1 = 0
            self._shot2 = 0
            self._shot3 = 0
            # total pins hit during the frame
            self._pin_total = 0
            # each shot has a strike indicator to distinguish 
            # between multiple strikes in the final frame.
            self.shot1_strike = False
            self.shot2_strike = False
            self.shot3_strike = False
            self.spare = False
            # the number of pins remaining, which can be reset up to two times on the final frame.
            self._pins_remaining = PINS_PER_LANE
        
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
                # since this frame is done, the following score calculation is final
                self._scoring_complete = True

            frame_score = 0

            # score calculation for last frame. Shot3 is zero unless it was taken
            if self.index == LAST_FRAME_INDEX:
                frame_score = self.shot1 + self.shot2 + self.shot3
            else:
                if self.shot1_strike:
                    if self.next_frame.shot1_strike and self.index == (LAST_FRAME_INDEX - 1):
                        # second-to-last frame's strike
                        frame_score = self.shot1 + self.next_frame.shot1 + self.next_frame.shot2
                    elif self.next_frame.shot1_strike:
                        frame_score = self.shot1 + self.next_frame.shot1 + self.next_frame.next_frame.shot1
                    else:
                        frame_score = self.shot1 + self.next_frame.shot1 + self.next_frame.shot2
                elif self.spare:
                    frame_score = self.shot1 + self.shot2 + self.next_frame.shot1
                else:
                    frame_score = self.shot1 + self.shot2
            
            self._score = frame_score
            return frame_score

        @property
        def shot1(self):
            return self._shot1

        # state changes in the frame is accounted for in the shot.setter methods
        @shot1.setter
        def shot1(self, pins):
            if self._done:
                raise ValueError("Frame is somehow already finished before the 1st shot: " + str(self))
            elif pins > PINS_PER_LANE or pins < 0:
                raise ValueError("Invalid number of pins for shot 1. " + str(self))
            
            self._shot1 = pins
            self._pin_total = pins
            
            if pins == PINS_PER_LANE:
                self.shot1_strike = True
                if self.index == LAST_FRAME_INDEX:
                    # the last frame resets the pin count after a strike on shot1
                    self._pins_remaining = PINS_PER_LANE
                else:
                    self._pins_remaining = PINS_PER_LANE - pins
                    self._done = True
            else:
                self._pins_remaining = PINS_PER_LANE - pins
        
        @property
        def shot2(self):
            return self._shot2

        @shot2.setter
        def shot2(self, pins):
            if self.done:
                raise ValueError("Cannot set a value for shot2, frame is finished.\n" + str(self))
            
            pin_count_error = ValueError("Invalid number of pins after shot 2 for " + str(self))
            
            self._shot2 = pins
            self._pin_total += pins

            if self.index == LAST_FRAME_INDEX: # state changes if it is the last frame
                if pins == PINS_PER_LANE: #strike
                    self.shot2_strike = True
                    self._pins_remaining = PINS_PER_LANE
                elif self.pin_total == PINS_PER_LANE: # spare
                    self.spare = True
                    self._pins_remaining = PINS_PER_LANE
                elif self.pin_total < PINS_PER_LANE: # neither strike or spare
                    self._pins_remaining = PINS_PER_LANE - self.pin_total
                    self._done = True
                else:
                    raise pin_count_error
            else: 
                # state change logic for all frames except the last frame
                self._done = True
                self._pins_remaining = PINS_PER_LANE - self.pin_total
                if self.pin_total == PINS_PER_LANE: # spare
                    self.spare = True
                if self.pin_total > PINS_PER_LANE or self.pin_total < 0: # neither strike or spare
                    raise pin_count_error

        @property
        def shot3(self):
            return self._shot3

        @shot3.setter
        def shot3(self, pins):
            if self.index != LAST_FRAME_INDEX:
                raise IndexError(f"Frame has only two shots\n" + str(self))
            elif self.done:
                raise ValueError("Third shot is not allowed without a strike or spare\n" + str(self))
            elif pins > PINS_PER_LANE or pins < 0:
                raise ValueError("Invalid number of pins for " + str(self))
            else:
                self._shot3 = pins
                self._done = True
                self._pins_remaining = PINS_PER_LANE - pins
                if pins == PINS_PER_LANE:
                    self.shot3_strike = True
        
        def __str__(self):
            return f"Frame{self.index}(shot1={self.shot1}, shot2={self.shot2}, shot3={self.shot3}, scoring_complete={self._scoring_complete}, score={self.score})"

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

        while False in [b.done_bowling for b in self.bowlers]:
            for b in self.bowlers:
                b.bowl_frame(self.autoplay)
        
        print('Final Scores:')
        for b in self.bowlers:
            print(f"Player: {b.name}")
            print(str(b.frame_set), '\n')
    