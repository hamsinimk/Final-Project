# Monte Carlo Simulator

Name: Hamsini Muralikrishnan

## Code Examples

Importing the module
```python
import montecarlo
```
Calling the DieClass/ instantiating a die object
```python
mydie = montecarlo.DieClass(np.array([1 2 3 4 5 6]))
```

Changing the weight of face "3" on the die to 5 (it will be weighted 5 times more than the other faces) 
As a note, changing the weight is not necessary, but by default, all faces will have weights of 1/ will be equally weighted (fair die)
```python
mydie.change_weight(3, 5)
```

Roll the die 10 times - a list with the results of each roll will be returned
```python
mydie.roll_die(10)
```

Return the current state of the die - die faces and respective weights
```python
mydie.die_state()
```

Calling the GameClass / instantiating a game object

**If using the same die object as defined above or can redefine new die object(s) and pass through 1 or more die in GameClass
```python
mygame = montecarlo.GameClass(mydie, mydie)
```

Play the game with the defined die objects (which were passed through GameClass above) by rolling each die 10 times
```python
mygame.play(10)
```

Return the results of the recent play in a wide formatted dataframe (default)
```
mygame.recent_play()
```

Calling the AnalyzeClass / instantiating an analyze object
```python
myanalyze = AnalyzeClass(mygame)
```

Checking how many games resulted in jackpots 
```python
myanalyze.check_jackpot()
```

Checking how many of each face was rolled in each game/event in the passed game object
```python
myanalyze.face_counts()
```

Checking how many distinct combinations of faces rolled in the game object
```python
myanalyze.combo_count()
```

Checking how many distinct permutations of faces rolled in the game object
```python
myanalyze.perm_count()
```

API Description
