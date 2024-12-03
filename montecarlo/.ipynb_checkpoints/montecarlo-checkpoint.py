import numpy as np
import pandas as pd

class DieClass():
    """
    General definition: The DieClass is used to create a die object. This class will be used to first create a die 
    with any number of sides or faces and weights of each side default to 1. The user can also change the weight of any side, 
    one side at a time. Then, the die can be rolled a specified number of times and the state of the die, 
    which includes the faces and weights, can be returned.
    
    """
    
    def __init__(self, faces):
        """
        Purpose: The purpose of the __init__ method is to essentially create the die object as a pandas dataframe. 
        Input Argument(s): faces
            Faces is an np array that contains the faces of the die object you are creating. If you pass in 2 face or side
            values in the np array, then you will be creating a die of 2 sides, which is a coin. If you pass in 6 values in
            the np array, you will be creating a traditional die to play with later on. The faces array can contain integers
            or strings. Once the faces array is passed, a pandas dataframe is made with default weights of 1 for each side,
            making a "fair" dice and the index for the dataframe is set to the faces of the object. Furthermore, the weights
            in the dataframe are modified to be proportions so they are less than 1. 
        
        """
        if not isinstance(faces, np.ndarray):
            raise TypeError("you have to pass a numpy array!")
        if not all([isinstance(f, (np.int32, np.int64, np.str_, str)) for f in faces]):
            raise TypeError("you have to pass strings or integers!")
        if len(np.unique(faces)) != len(faces):
            raise ValueError("array should have distinct values!")
        self._die_df = pd.DataFrame({
            'faces': faces, 
            'weights': np.ones(len(faces), dtype=float)}
        ).set_index(['faces'])

    
    def change_weight(self, face_val, new_weight):
        """
        Purpose: The purpose of the change_weight method is to allow the user to change the weight of a single face or side
        of the die as the default weights are 1 for each side, as mentioned above. The weight of each side can only be 
        altered one at a time. By doing this, you can create an "unfair" dice. Using the specified face value, which is the
        index of the dataframe, the weight is changed to the new weight. 
        
        Input Arguments: 
        face_val: The user will pass the face or side that they want to change the weight for. The method will make 
        sure that the face value that's passed is already in the die array. 
        new_weight: The new weight is specified, which should be a numeric or castable as a numeric. The method checks if 
        it is a numeric or castable as a numeric and raises an error if not. 
        
        """
        if face_val not in self._die_df.index:
            raise IndexError("this is not a valid face value!")
        if not str(new_weight).isnumeric():
            raise TypeError("new weight is not numeric")
        self._die_df.loc[face_val, 'weights'] = new_weight
        
    def roll_die(self, num_rolls=1):
        """
        Purpose: The purpose of the roll_die method is to roll the die based on the weights of each face. The die is rolled
        by using random sampling with replacement based on the weights. The results of the roll won't be saved, but 
        the method will return a list of the face values that were rolled. 
        
        Input Arguments:
        num_rolls: Any number of rolls can be specified here to roll the die. The default value for the number the rolls is 1, so if no
        value is passed, the die will be rolled once. 
        
        Return Values: roll_die returns a list of the faces that were rolled depending on the number of rolls specified 
        by the user. The method uses random sampling with replacement to do so and takes the weights that were 
        specified by the user previously into account. This list is not internally saved. 
        """
        self._die_df['weights'] = self._die_df['weights']/np.sum(self._die_df['weights'])
        return list(np.random.choice(self._die_df.index, num_rolls, replace = True, p = self._die_df['weights']))
        
    def die_state(self):
        """
        Purpose: The purpose of the die state is just to return the private die dataframe. Essentially, the user will be
        able to see the faces of the die and the associated face values. 
        
        Input Arguments: None
        
        Return Values: The die_state method will return the private dataframe containing the faces of the die and 
        the associated weights. 
        """
        return self._die_df

class GameClass():
    """
    General definition: The GameClass is used to simulate a game in which one or more similar die are rolled. The die are "similar" in that
    if multiple die objects are passed, they must have the number of sides and associated face values. But, if the user chooses to do so,
    the weight values of the faces can be different between the die objects. 
    """
    def __init__(self, die_obj):
        """
        Purpose: The __init__ method takes a list of already instantiated die object(s).  
        
        Input Arguments:
        die_obj: The die object consists of a list of die that are instantiated using the previous DieClass. The list can be specified 
        prior to passing it through GameClass(), for ease, or can be done simultaneoulsy while passing it through GameClass.
        """
        self.die_obj = die_obj
    def play(self,num_rolls):
        """
        Purpose: The play method is used to roll each dice in the die_obj specified above. Essentially, the method from
        DieClass (roll_die) is invoked to roll each die and the results of each roll are saved to a dataframe that include
        the number of the roll as the index with each die number (based on its index in the passed list) as the columns and 
        the face value that is rolled in each cell. This described layout for the dataframe follows a wide format.
        Unlike the roll_die method in DieClass, the results are saved.
        
        Input Arguments: 
        num_rolls: The number of rolls is again specified here to roll each die a specific number of times using the roll_die
        method from DieClass. 
        
        """
        roll_results = []
        for die in self.die_obj:
            roll_results.append(die.roll_die(num_rolls))
        self._play_df = pd.DataFrame(roll_results).T
        self._play_df.columns = [f'Die {i}' for i in range(len(self.die_obj))] 
        self._play_df['roll number'] = range(1, num_rolls+1)
        self._play_df = self._play_df.set_index(['roll number'])
    def recent_play(self,format_play='wide'):
        """
        Purpose: The purpose of the recent_play method is to return the results of the game to the user based on the format
        that they specify. The two options for the returned dataframe are wide or narrow. 
        
        Input Arguments:
        format_play: The format of the returned dataframe can be either wide or narrow. As defined above in the play method,
        the dataframe is constructed with a wide format, which is the default value for the argument. The user can specify
        narrow if they want to change the format from the default. If an argument other than narrow or wide is provided, a
        ValueError is raised and nothing will be returned. 
        
        Return Values: Based on the input argument, a wide or narrow dataframe containing the die number, roll number and 
        roll result will be returned to the user. 
        
        """
        if format_play == 'narrow':
            play_df_reset = self._play_df.reset_index()
            narrow_df = pd.melt(play_df_reset, id_vars = 'roll number', value_vars = self._play_df.columns,
                               var_name = 'Die', value_name = 'roll result')
            narrow_df = narrow_df.set_index(['roll number', 'Die'])
            return narrow_df
        elif format_play == 'wide':
            return self._play_df
        else:
            raise ValueError('the only table format options are either wide (default) or narrow!')                                                        
class AnalyzeClass():
    """
    Purpose: The Analyze Class takes the results of a game (game object) and analyzes it for different statistical
    properties. 
    """
    def __init__(self, game_obj):
        """
        Purpose:
        The purpose of the __init__ method is to just take the game object as an input parameter to use in the AnalyzeClass.
        
        Input Arguments:
        game_obj: This is the game object made from the previous Game Class. The play method should be used prior to passing the game
        object and its results are passed through the Analyze Class. If the game that is passed is not an Game object, then a ValueError is
        raised. 
        """
        if not isinstance(game_obj, GameClass):
            raise ValueError('Passed value is not a Game object!')
        self.game_obj = game_obj
        self.play_df = self.game_obj._play_df
    def check_jackpot(self):
        """
        Purpose:
        The jackpot method checks/ calculates how many times a game resulted in a jackpot (when all sides of the 
        die that are rolled are the same). 
        
        Input Arguments:
        None
        
        Return Values:
        This method returns the number of times a game in the game object resulted in a jackpot. This is returned as an
        integer. If none of the games result in a jackpot, the method returns that there are no jackpots. 
        
        """
        num_jackpot = 0
        for _, row in self.play_df.iterrows():
            if (row==row[0]).all():
                num_jackpot+=1
        if num_jackpot == 0:
            print('No jackpots this game!')
        return num_jackpot

    def face_counts(self):
        """
        Purpose:
        The face_counts method returns the number of times each face of the die is rolled for each game/event in the game
        object. 
        
        Input Arguments:
        None
        
        Return Values:
        The face_counts method returns a dataframe that includes the counts of each face for each event/game in the game
        object. The roll number is the index, while the columns are the face values of the die with each cell containing
        the value count for that face in that game/event. This format for the returned dataframe follows a wide format. 
        """
        face_count_df = self.play_df.apply(lambda row: row.value_counts(), axis=1)
        face_count_df = face_count_df.fillna(0).astype(int)
        return face_count_df
    
    def combo_count(self):
        """
        Purpose: The combo_count method calculates the distinct combinations of faces rolled in the game object.
        
        Input Arguments: 
        None
        
        Return Values: The combo_count method returns a dataframe with the distinct combinations along with their 
        counts. This dataframe has a MultiIndex of the distinct combinations and a column of the associated counts 
        for these disinct combinations. In this case, order does not matter. 
        """
        combo_count_df = self.play_df.apply(lambda row: tuple(np.sort(row)), axis = 1).value_counts().to_frame('n')
        combo_count_df.index = pd.MultiIndex.from_tuples(combo_count_df.index)
        return combo_count_df

    def perm_count(self):
        """
        Purpose: The perm_count method calculates the distinct permutations of faces rolled in the game object.
        
        Input Arguments: 
        None
        
        Return Values: The perm_count method returns a dataframe with the distinct permutations along with their 
        counts. This dataframe has a MultiIndex of the distinct permutations and a column of the associated counts 
        for these disinct permutations. In this case, order does matter. 
        """
        perm_count_df = self.play_df.apply(lambda row: tuple(row), axis = 1).value_counts().to_frame('n')
        perm_count_df.index = pd.MultiIndex.from_tuples(perm_count_df.index)
        return perm_count_df
    