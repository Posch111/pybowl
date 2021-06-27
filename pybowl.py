import random

LAST_FRAME_INDEX = 9
PINS_PER_FRAME = 10

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
            self.current_frame = self.frame_set.frames[0]
        else:
            self.current_frame = self.current_frame.next_frame

        frame = self.current_frame
        print(f"{self.name}, bowl frame {frame.index + 1}.")
        frame.shot1 = self.roll_ball(pins_remaining=PINS_PER_FRAME, autoplay=autoplay)
        if not frame.strike:
            print(f"You hit {frame.shot1} pin(s). Roll again.")
            frame.shot2 = self.roll_ball(pins_remaining=(PINS_PER_FRAME - frame.shot1), autoplay=autoplay)
        elif frame.strike and frame.index != LAST_FRAME_INDEX:
            if frame.strike
        
        if frame.index != LAST_FRAME_INDEX:
            total_pins = frame.shot1 + frame.shot2
            if total_pins < 0 or total_pins > PINS_PER_FRAME :
                raise ValueError(f"Invalid number of pins knocked in a single frame: {total_pins}"
                                "shot1_pins: {shot1_pins}, shot2_pins: {shot2_pins}")
        else:
            total_pins = frame.shot1 + frame.shot2 + frame.shot3
            if total_pins < 0 or total_pins > PINS_PER_FRAME :
                raise ValueError(f"Invalid number of pins knocked in a single frame: {total_pins}"
                                "shot1_pins: {shot1_pins}, shot2_pins: {shot2_pins}")


        bowl_phrase = ''
        if frame.strike:
            bowl_phrase = 'a strike.'
        elif frame.spare:
            bowl_phrase = 'a spare.'
        else:
            bowl_phrase = f"a total of {total_pins} pin(s) this frame."

        print(f"{self.name} bowled {bowl_phrase}")

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
            # print("current=" + str(frame) + " next= " + str(frame.next_frame) + "\n")

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
            self._pin_total = 0
            self.strike = False
            self.spare = False
        
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
        def score(self):
            if self._scoring_complete:
                return self._score
            elif self._done:
                _scoring_complete = True
            
            frame_score = 0
            if self.index == LAST_FRAME_INDEX:
                return self.pin_total
            elif self.strike:
                frame_score += PINS_PER_FRAME
                if self.next_frame.strike:
                    frame_score += self.next_frame.score + self.next_frame.next_frame.score
                    self._scoring_complete = True
                else:
                    frame_score += self.next_frame.score
            elif self.spare:
                frame_score += PINS_PER_FRAME + self.next_frame.shot1
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
            elif pins > PINS_PER_FRAME or pins < 0:
                raise ValueError("Invalid number of pins after shot 2 for " + str(self))
            
            if pins == PINS_PER_FRAME:
                self.strike = True
                self._done == True
            self._shot1 = pins
            self._pin_total += pins
        
        @property
        def shot2(self):
            return self._shot2

        @shot2.setter
        def shot2(self, pins):
            if self.done:
                raise ValueError("Cannot set a value for shot2, frame is finished.\n" + str(self))
            elif (self._shot1 + pins) > PINS_PER_FRAME or (self._shot1 + pins) < 0:
                raise ValueError("Invalid number of pins after shot 2 for " + str(self))
            
            self._shot2 = pins
            self._pin_total += pins

            if (self._shot1 + self._shot2) == PINS_PER_FRAME:
                self.spare = True
                # only the last frame has a third shot when all pins are knocked
                if self.index != LAST_FRAME_INDEX:
                    self._done = True

        @property
        def shot3(self, pins):
            return self._shot3

        @shot3.setter
        def shot3(self, pins):
            if self.index != LAST_FRAME_INDEX:
                raise IndexError(f"Frame has only two shots\n" + str(self))
            elif self.frame_complete:
                raise ValueError("Third shot is not allowed without a strike or spare\n" + str(self))
            elif pins > PINS_PER_FRAME or pins < 0:
                raise ValueError("Invalid number of pins for " + str(self))
            else:
                _shot3 = pins
                self.done = True
        
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

    
    # def bowl_player(self, player):
