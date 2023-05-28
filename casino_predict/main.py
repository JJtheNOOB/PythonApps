import scipy.stats as scs

class die:
    def __init__(self, color, num) -> None:
        if color not in ["black", "red", "zero", "double_zero"]:
            raise ValueError("Color value not permitted!")
        if num not in [i for i in range(37)]:
            raise ValueError("Number value not permitted!")
        self.color = color
        self.num = num

class casino_machine:
    def __init__(self) -> None:
        self.seq = []   # memorize the sequence number
        self.basic_percentage = 18 / 40  # basic percentage of getting red or black etc
        self.seq_lookback = 5  # specify how many numbers we wanted to look back for
        self.percent_dict = {
            "red_percen" : self.basic_percentage,
            "black_percen" : self.basic_percentage,
            "small_percen" : self.basic_percentage,
            "large_percen" : self.basic_percentage,
            "even_percen" : self.basic_percentage,
            "odd_percen" : self.basic_percentage,
            "zero_percen" : 1 / 40,
            "double_zero_percen" : 1 / 40
        }
    
    def clear_seq(self):
        """
        clean the seq & initialize the dict
        """
        self.seq = []
        self.percent_dict = self.percent_dict = {
            "red_percen" : self.basic_percentage,
            "black_percen" : self.basic_percentage,
            "small_percen" : self.basic_percentage,
            "large_percen" : self.basic_percentage,
            "even_percen" : self.basic_percentage,
            "odd_percen" : self.basic_percentage,
            "zero_percen" : 1 / 40,
            "double_zero_percen" : 1 / 40
        }

    def predict(self):
        """
        return the most confident selections with probabilities for the next prediction
        """
        if len(self.seq) > 0:
            print("The last sequences numbers are as follows:")
            print([(die.color, die.num) for die in self.seq])
        else:
            print("Sequence is empty...")
        print("Please try the following numbers:")
        max_percentage = max(self.percent_dict.values())
        predict = [k for k,v in self.percent_dict.items() if v == max_percentage]
        final_msg = ""
        for val in predict:
            if "red" in val:
                final_msg += "Red, "
            if "black" in val:
                final_msg += "Black, "
            if "small" in val:
                final_msg += "Small, "
            if "large" in val:
                final_msg += "Large, "
            if "even" in val:
                final_msg += "Even, "
            if "odd" in val:
                final_msg += "Odd, "
        final_msg = final_msg[:-2]
        final_msg += " with chance of {}%".format(round(max_percentage * 100),2)
        return final_msg
    
    def enter_seq(self, die):
        """
        Add the last drawed value into the sequence
        Update percentage of all values
        Input: die object which has an attribute of color and number
        """
        self.seq.append(die)
        if len(self.seq) < self.seq_lookback:
            seq_consider = self.seq
        else:
            seq_consider = self.seq[:self.seq_lookback]
        len_seq = len(seq_consider)
        num_red = 0
        num_even = 0
        num_small = 0
        num_zero = 0
        num_double_zero = 0
        for single_die in seq_consider:
            if single_die.color == "red":
                num_red += 1
            elif single_die.color == "zero":
                num_zero += 1
            elif single_die.color == "double_zero":
                num_double_zero += 1
            if single_die.color != "zero" and single_die.color != "double_zero" and single_die.num % 2 == 0:
                num_even += 1
            if single_die.color != "zero" and single_die.color != "double_zero" and single_die.num <= 18:
                num_small += 1
        # update percent dict
        non_norm_red = scs.binom.pmf(num_red + 1, len_seq + 1, self.basic_percentage)
        non_norm_black = scs.binom.pmf((len_seq - num_red - num_zero - num_double_zero) + 1, len_seq + 1,  self.basic_percentage)
        non_norm_small = scs.binom.pmf(num_small + 1, len_seq + 1, self.basic_percentage)
        non_norm_large = scs.binom.pmf((len_seq - num_small - num_zero - num_double_zero) + 1, len_seq + 1, self.basic_percentage)
        non_norm_even = scs.binom.pmf(num_even + 1, len_seq + 1, self.basic_percentage)
        non_norm_odd = scs.binom.pmf((len_seq - num_even - num_zero - num_double_zero) + 1, len_seq + 1, self.basic_percentage)
        # normalizing percentage
        self.percent_dict["red_percen"] = non_norm_red / (non_norm_red + non_norm_black)
        self.percent_dict["black_percen"] = non_norm_black / (non_norm_red + non_norm_black)
        self.percent_dict["small_percen"] = non_norm_small / (non_norm_small + non_norm_large)
        self.percent_dict["large_percen"] = non_norm_large / (non_norm_small + non_norm_large)
        self.percent_dict["even_percen"] = non_norm_even / (non_norm_even + non_norm_odd)
        self.percent_dict["odd_percen"] = non_norm_even / (non_norm_even + non_norm_odd)
        # print(self.percent_dict)


if __name__ == "__main__":
    cm = casino_machine()
    die_1 = die("red", 36)
    die_2 = die("black", 25)
    die_3 = die("black", 25)
    die_4 = die("black", 25)
    die_5 = die("black", 25)
    cm.enter_seq(die_1)
    cm.enter_seq(die_2)
    cm.enter_seq(die_3)
    cm.enter_seq(die_4)
    cm.enter_seq(die_5)
    # cm.clear_seq()
    print(cm.predict())