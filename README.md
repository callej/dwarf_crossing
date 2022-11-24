# Dwarf Crossing

This program is based on a math problem that was published in a newspaper. It is similar to the Bamse problem where the tortoises Professor Shellback and Achilles as well as the bunnies Little Frisky and Bugs Bunny are all trapped in a dark cave. They only have one flashlight and they will need to get out of the cave before the flashlight goes out. 

The dwarf crossing is similar, but in this case there are 300 dwarfs that need to cross a bridge under certain constraints, and we are to find the optiomal solution that leads to the shortest crossing time in total for all 300 dwarfs to cross the bridge.

This repository has two different programs that uses different approaches to find a solution to the Dwarf Crossing problem:
1. Random <br/>
While this is extremely unlikely to produce the optimal result, it is an extremely quick and easy way to get a picture of the problem, see the trends, and get some ideas about in which range the optimal result could be. This approach is found in random_dwarf.py
2. Greedy <br/>
This is another very quick and easy way to get a result, since it only takes the best option available at each stage instead of looking if there is a better solution overall by using a strategy that takes the whole picture into account. For this reason a greedy approach to a problem may be a risky strategy and it is only under certain conditions a greedy approach will give the optimal solution. However, from a found solution it might be possible to verify that there can't be a better solution. If so, then it is proven that the found solution is the optimal solution. This approach is found in greedy_min_dwarf.py

<br/>

## The Problem

There are 300 dwarfs that need to cross a bridge in the middle of the crispy cold polar night.
It is a rickety bridge in poor condition which only holds for at most two dwarfs to cross at a time.
With the cloudy sky it is pitch dark and they only have one lantern, which they need in order to cross the bridge.
If two dwarfs crosses the bridge together someone has to bring the lantern back for the others to be able to cross.
However, no dwarf wants to cross the bridge more than 3 times (i.e. over, back and over again).
Each dwarf requires different amount of time to cross the bridge: 1 min, 2 min, 3 min, …, up to 300 min
for the slowest dwarf. When two dwarfs walk together, they walk in the slowest pace.
What is the fastest time they can cross the bridge for all 300 to be on the other side, and how will they achieve this?

<br/>

### Random Approach

The code is in the file random_dwarf.py

This approach is completely random and uses only probability to find better solution. No other strategy or optimization is involved.

#### Implementation Algorithm:
1. Select two dwarfs randomly at the start position
2. Add to the total time the longest crossing time for the two dwarfs
3. At finnish, select a dwarf at random that hasn't crossed the bridge three time, to walk back with the lantern
4. Add to the total time the crossing time for this dwarf
5. Continue step 1 - 4 until all dwarfs have crossed the brigde
6. Save the total time in an array
7. Keep doing runs by repeating the steps 1 - 5 over and over again
8. After each run check if the total time is less than what is last saved in the array. If so, this is a better solution. Add the total time to the array.
9. After all the runs are done the array will consist of total crossing times that are consistantly improved, showing a trend towards an optimal result.
10. Repeat steps 1 - 9 to collect many trend arrays
11. Plot the arrays in a graph to get a picture of how well this approach will find better solutions, how more runs will affect, and in which range the optimal solution might be. 

The more tries used will get a better result and the more arrays plotted will get a better understand on how this approach behaves where the optimal result might be. Just from a very few runs, e.g. 1000 runs, repeated 25 times, the best solutions approaches 100 000 minutes, with the curve still sloping down. It is obvious that the expected optimal solution should be some distance below 100 000 minutes.

![Random Dwarf Results - 300 Dwarfs](https://user-images.githubusercontent.com/1498298/203844294-8ef27865-0960-4402-bb95-03f41dc47f02.png)


<br/>

### Greedy Approach

The code is in the file greedy_min_dwarf.py

Solution Strategy:
1. Minimize the average of the difference in speed when two dwarfs walk together over the bridge.
2. Minimize the average of the time it take for the dwarfs that need to walk back with the lantern.

The reason for number 1 is that we want to waste as little as possible of a faster dwarf's speed. The speed is given
by the time it takes for a dwarf to cross the bridge. Since all the dwarfs required different amount of time to
cross the bridge the difference in time between two dwarfs will always be at least 1 minute, meaning that the
faster dwarf will have to walk 1 minute slower that what he could. He is loosing one minute. We want to minimize
that loss over all the dwarfs that are crossing. Since it will always be at least 1 minute difference between any
two dwarfs, the average cannot be less that 1 minute. We will aim for an average of 1 minute. If we reach this we
know that we have minimized the time it took for the dwarfs to cross the bridge, which is half the problem, and
which is the reason for number 1 above.

The other half of the problem is that we want to minimize the time it takes for the dwarfs to walk back with the
lantern. This can be done by always making sure that the fastest dwarf that still has crossings left will be on
the other side of the bridge ready to walk back with the lantern.


#### Implementation Algorithm: <br/>
Note: <br/>
Even though this problem is well structured and clearly defined I will create a generic implementation where
      the number of the dwarfs can vary, their time to cross can be changed, the maximum crossings can be changed,
      and the maximum number of dwarfs that can cross the bridge together can be changed.
      The two reasons for this are: <br/>
      a) The structure and the logic in the code becomes more clear when things are defined in one place instead
         of hardcoded all over the program. The logic also becomes more obvious when the code explicitly shows
         the decisions made. <br/>
      b) It is possible to test the algorithm with other conditions very easily and do other experiments.
         However, pay attention to that this is a greedy algorithm, which a risky way to solve a problem and
         also very likely to fail outside of its domain. A domain that is difficult to know exactly.

The steps of the algorithm: <br/>
1. All dwarfs will be sorted after their speed, i.e. after how much time they need to cross the bridge.
2. To start, the two fastest dwarfs will cross the bridge in order to have the fastest dwarf available to
   walk back with the lantern.
3. The fastest of the dwarfs that crossed will walk back with the lantern.
4. Check where the fastest dwarf with at least enough crossings left is located.
   If dwarf is before the bridge (at start), at least 3 crossings left are required. Otherwise the dwarf can't
   go back with the lantern, so the speed is of no benefit.
   If the dwarf is after the bridge (at finish), at least 2 crossings left are required for the same reason. <br/>
   4a) If that is before the bridge and we don't waste a faster dwarf to come back with the lantern,
       send that dwarf over together with the second fastest dwarf available <br/>
   4b) If that is after the bridge, find the two dwarfs with the least difference in speed. If there are several,
       send the two fastest.
5. Send the fastest dwarf with enough (which is 2) crossings left back with the lantern.
6. Repeat step 4 and 5 until there are no more dwarfs available to cross.
7. Keep track of the crossing times: <br/>
   7a) When dwarfs cross together we are aiming for an average of the difference in speed of 1 minute <br/>
   7b) For the returning dwarfs we are aiming for an average of (1 + number of returns) / 2 <br/>
   7c) Note that these numbers are only valid when the problem is structured as described above, with
       the fastest dwarf crossing the bridge in 1 minute, and when it is always a difference of 1 minute in speed
       between dwarfs next to each other when ordered after their speed, and that the maximum number of
       crossings are 3 for all the dwarfs.
8. Print the result: <br/>
   8a) Print the time it took for all the dwarfs to cross <br/>
   8b) Print the scheme showing how the dwarfs crossed the bridge back and forth <br/>
   8c) Print if this is an optimal result as aimed for in point 7 above <br/>

<br/> 

Running this program we can see that the result is 89551 minutes.

Now we can see that we never lost more than 1 minute in each crossing of two dwrafs. And we can see that the return time is the smallest possible. This means that the result we received of 89551 is the shortest possible time and that we have found an optimal strategy for the dwarfs to cross the bridge.

<br/>


### The Math

With the same stragegy we can also do the math directly. The stragey is: <br/>
1. Cross the bridge with two dwarfs the has the least difference in crossing time. Of those options, take the pair with the shortest crossing time available.
2. Bring back the fastest dwarf.
3. Keep doing this until all dwarfs have crossed the bridge.

The result will look like this:

| Move # | Time       | Action                                    |
|:------:|:----------:|:-----------------------------------------:|
|     1  |     2 min  | Dwarf 1 and 2                             |
|     2  |     1 min  | Dwarf 1 return                            |
|     3  |     4 min  | Dwarf 3 and 4                             |
|     4  |     2 min  | Dwarf 2 return                            |
|     5  |     2 min  | Dwarf 1 and 2 (1 and 2 are done)          |
|     6  |     3 min  | Dwarf 3 return                            |
|     7  |     6 min  | Dwarf 5 and 6                             |
|     8  |     4 min  | Dwarf 4 return                            |
|     9  |     4 min  | Dwarf 3 and 4 (3 and 4 are done)          |
|    10  |     5 min  | Dwarf 5 return                            |
|    11  |     8 min  | Dwarf 7 and 8                             |
|    12  |     6 min  | Dwarf 6 return                            |
|    13  |     6 min  | Dwarf 5 and 6 (5 and 6 are done)          |
|    14  |     7 min  | Dwarf 7 return                            |
|    15  |    10 min  | Dwarf 9 and 10                            |
|    16  |     8 min  | Dwarf 8 return                            |
|    17  |     8 min  | Dwarf 7 and 8 (7 and 8 are done)          |
|    18  |     9 min  | Dwarf 9 return                            |
|    19  |    12 min  | Dwarf 11 and 12                           |
|    20  |    10 min  | Dwarf 10 return                           |
|    21  |    10 min  | Dwarf 9 and 10 (9 and 10 are done)        |
|    .   |     .      |       .                                   |
|    .   |     .      |       .                                   |
|    .   |     .      |       .                                   |
|   593  |   296 min  | Dwarf 295 and 296 (295 and 296 are done)  |
|   594  |   297 min  | Dwarf 297 return                          |
|   595  |   300 min  | Dwarf 299 and 300                         |
|   596  |   298 min  | Dwarf 298 return                          |
|   597  |   298 min  | Dwarf 297 and 298 (297 and 298 are done)  |


<br/>

There is an obvious pattern:
  * The return time will be: 1 + 2 + 3 + ... + 297 + 298 = 298 * (1 + 298) / 2 = 44 551 min
  * The crossing time will be: 2 + 2 + 4 + 4 + 6 + 6 + ... + 298 + 298 + 300 = 298 * (2 + 298) / 2 + 300 = 45 000 min
  
<br/>

Note that dwarf 299 and 300 never have to return to bring someone else over since all dwarfs are already on the other side after that dwarf 297 and 298 have crossed. They only have to cross once. That is why the return times are only from 1 to 298 min and that there is only on crossing time that is 300 min.

Again, this can be proven to be the optimal solution, since: 
* They have to return 298 times to be able to get 300 over the bridge, and the smallest amount of time since they only can return once is 1 + 2 + 3 + ... + 298.
* You can never to better than loosing 1 minute per couple crossing the bridge, and the smallest option to make this happen is 2 + 2 + 4 + 4 + ... + 298 + 298 + 300.


Doing the math shows that the optimal solution will give a total crossing time of 44 551 + 45 000 = 89 551 min.

This is the same result as the greedy approach gave using the Python implemented algorithm.


## End Note

As what is obvious from above is that the easiest way to solve this and to prove that this is the optimal solution would be the math approach. However, the key take away is that by writing simple programs you can investigate problems easily in different ways to get a better understanding of the behavior of the problem domain and what to expect from a solution. For more difficult problems this can be very useful insights. Most interesting might be how you can use Python to create a model of the problem exactly as you would like it to be, and exactly in the way you would like to treat the problem. Some key things to take from this is:
1. The classes created that reflect the physical objects and their behavior.
2. The way to overload operators in order to make the obejcts able to use  regular operators making the code more logical, shorter, clearer and easier to understand.
3. The ability to create custom exceptions with all information needed to have detailed knowledge of the conditions when an exception occur, being able to take the correct action and provide the most informative information.
4. How to write test cases that verifies all the expected functionality, making the results from the actual run of the program much more trustworty.

In summary, modeling and investigating problems using Python is easy and can provide a clean and efficient structure that can easily be modified to allow for further explorations.

<br/>
