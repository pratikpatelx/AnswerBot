class PositionHandler(object):
    "PositionHandler: This class implements the paragraph position under the user oriented features"
    def calc_position(self, position):
        """
        calc_position(position):
        This method calculates the paragraph's summary value which is to be 
        inversely proportional to the paragraph's position in the post for the
        first m paragraphs
        """
        position_score = 0
        if position >=1 and position <=3:
            position_score = 1 / position
        else:
            position_score = 0
        return position_score

if __name__ == "__main__":
    test = PositionHandler()
    position = 1
    x = test.calc_position(position)
    print(x)