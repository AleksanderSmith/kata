import unittest

class Bowling():
  def is_blank(self, throw):
      return throw == '-'
        
  def is_spare(self, frame):
    return frame[1] == '/'
    
  def is_strike(self, frame):
    return frame[0] == 'x' or frame[0] == 'X'
  
  def score_line(self, line):
    frames = self.get_frames(line)
    frame_index = 0
    score = 0
    for frame in frames:
      
      if self.is_strike(frame):
        score += self.handle_strike(frames, frame_index)
        
      elif self.is_spare(frame):
        score += self.score_spare_frame(frame, frame_index)
        
      else:
        score += self.score_frame(frame)
        
      frame_index += 1
  
  def get_frames(self, line):
    scores = line.split(' ')
    frames = self.group_frames(scores)
    return frames

  def group_frames(self, scores):
    frame_size = 2
    return [scores[n:n+frame_size] for n in range(0, len(scores), frame_size)]
        
  def score_frame(self, frame):
    total = 0
    for score in frame:
      if not self.is_blank(score):
        total += score
      
    return total
  
  def score_spare_frame(self, frames, frame_index):
    score = 10
    if self.is_strike(frames[frame_index + 1]):
      score += 10
    elif not self.is_blank(frames[frame_index + 1][0]):
      score += frames[frame_index + 1][0]
    return score

  def get_extra_frames(self, frames, param_size):
    if type(frames[0]) == list:
      next_frame = frames[1]
      if(param_size > 2):
        frame_after_next = frames[2]
        return next_frame,frame_after_next
      else:
        return next_frame, None
    else:
      return frames

  def score_strike_frame(self, *frames):
    score = 10
    param_size = len(frames)
    next_frame, frame_after_next = self.get_extra_frames(frames, param_size)
    
    if self.is_spare(next_frame):
      score += 10
      return score
      
    if self.is_strike(next_frame):
      score += 10
      if frame_after_next is not None and self.is_strike(frame_after_next):
        score += 10
      else:
        if frame_after_next[0] != '-':
          score += frame_after_next[0]
          return score
        
    if self.is_blank(next_frame[0]):
      if not self.is_blank(next_frame[1]):
        score += next_frame[1]
    else:  
      score += next_frame[0]
    
    return score

    
  def handle_strike(self, frames, frame_index):
    if frame_index <= len(frames) - 2:
      score = self.score_strike_frame(frames[frame_index], frames[frame_index + 1], frames[frame_index + 2])
    elif frame_index <= len(frames) - 1:
      score = self.score_strike_frame(frames[frame_index], frames[frame_index + 1])
    else:
      score = self.score_strike_frame(frames[frame_index])
    return score
      

class test_get_frame_score(unittest.TestCase):
  def setUp(self):
    self.bowling = Bowling()
  
  def test_should_sum_score(self):
    self.assertEqual(self.bowling.score_frame([1,2]), 3, "Should be 3")
    self.assertEqual(self.bowling.score_frame([5,3]), 8, "Should be 8")
    self.assertEqual(self.bowling.score_frame([2,7]), 9, "Should be 9")
    self.assertEqual(self.bowling.score_frame([4,3]), 7, "Should be 7")
    self.assertEqual(self.bowling.score_frame([0,0]), 0, "Should be 0")
    self.assertEqual(self.bowling.score_frame([9,1]), 10, "Should be 10")
    
  def test_should_accept_dash_for_zero(self):
    self.assertEqual(self.bowling.score_frame([1, '-']), 1, "Should be 1")

  def test_should_accept_spare(self):
    self.assertEqual(self.bowling.score_spare_frame([[5,'/'], [5, 1]], 0), 15, "Should be 15")
    
  def test_should_accept_strike_followed_by_two_throws(self):
    self.assertEqual(self.bowling.score_strike_frame(['x', '-'], ['-', 1]), 11, "Should be 11")
  
  def test_should_add_next_throw_to_spare(self):
    self.assertEqual(self.bowling.score_spare_frame([[1, '/'], [1, 1]], 0), 11, "Should be 11")

  # def test_should_add_next_two_throws_to_strike(self):
  #   strike_frame = ['x', '-']
  #   self.assertEqual(Bowling.is_strike(strike_frame, strike_frame[0]))
    # self.assertEqual(Bowling.score_frame())

# Frame tests
class test_get_frames(unittest.TestCase):
  def setUp(self):
    self.bowling = Bowling()
    
  def test_should_get_frames(self):
    self.assertEqual(len(self.bowling.get_frames("2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")), 10, "should be 10")
    
  def test_should_accept_slash_for_spare(self):
    self.assertEqual(len(self.bowling.get_frames("2 / 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")), 10, "should be 10")
    
  def test_should_accept_x_for_slash(self):
    self.assertEqual(len(self.bowling.get_frames("2 / X 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2")), 10, "should be 10")
    
if __name__ == '__main__':
  unittest.main()
