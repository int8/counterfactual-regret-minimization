## Implementation of counterfactual regret minimization algorithm for Kuhn poker in python

This is supplementary code for [Counterfactual regret minimization blog post here](https://int8.io/counterfactual-regret-minimization-for-poker-ai)


to install:
```
pip install -r requirements.txt
```


to run:

```python
from common.constants import CARDS_DEALINGS
from games.kuhn import KuhnRootChanceGameState
from games.algorithms import ChanceSamplingCFR, VanillaCFR


root = KuhnRootChanceGameState(CARDS_DEALINGS)
chance_sampling_cfr = ChanceSamplingCFR(root)
chance_sampling_cfr.run(iterations = 1000)
chance_sampling_cfr.compute_nash_equilibrium()
# read Nash-Equilibrum via chance_sampling_cfr.nash_equilibrium member
# try chance_sampling_cfr.value_of_the_game() function to get value of the game (-1/18)

# vanilla cfr
vanilla_cfr = VanillaCFR(root)
vanilla_cfr.run(iterations = 1000)
vanilla_cfr.compute_nash_equilibrium()

# read Nash-Equilibrum via vanilla_cfr.nash_equilibrium member
# try vanilla_cfr.value_of_the_game() function to get value of the game (-1/18)

```

to run simple tests:
```python
pytest tests/
```
