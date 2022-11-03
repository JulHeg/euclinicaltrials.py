# euclinicaltrials.py

Since January 2022, the European Commission and the European Medicines Association are providing a new database for clinical trials called the Clinical Trial Information System (CTIS). It is publically accessible on the website [https://euclinicaltrials.eu](https://euclinicaltrials.eu).

Unfortunately, this database does not have a machine-readable interface for the public, only an API for EU member states. This package aims to make it easier for people to use the database by doing the annoying web scraping.

## Installation

To use this package, download the folder called 'euclinicaltrials' and put it in your PYTHONPATH. Or you can install it with pip and 
```
pip install -e git+https://github.com/JulHeg/euclinicaltrials.py.git#egg=euclinicaltrials
```

## Usage

Get a list of all clinical trials by id:

```python
from euclinicaltrials import CTIS, Trial

trial_ids = CTIS.get_all_trial_numbers()
```

Get a list of which member states the trial happens in:

```python
trial = Trial(trial_ids[0])
print(trial.member_states_concerned())
```

There is a longer example in the file [example.ipynb](example.ipynb).

The class `Trial` represents a single trial defined by its id. Because information on the trial is distributed over several pages on [https://euclinicaltrials.eu](https://euclinicaltrials.eu), the evaluation is lazy. When you access a property of a trial (like `member_states_concerned()`) from a page that has not been loaded yet, that page will be accessed from the website. That will take about a second or two.

The file `CTIS` contains helper methods for accessing the database as a whole.

## State of this package

This package does not (yet) cover all information about a trial. Partly this is because CTIS is still new. For example, no trials have reported results yet. So I don't know how they could be scraped.

As with any web scraping, a lot of this could break anytime if the website changes, but I will try to keep things up-to-date. If this package is not working, is missing something you need, or you have any other comments, please do not hesitate to open an issue or contact me!

## Credit
This work is inspired by others, like the [Clinical Trials Python API](https://github.com/codeforamerica/clinical_trials_python) for the USA's [clinicaltrials.gov](https://clinicaltrials.gov/). In particular, I would like to thank [the TrialsTracker Project](https://www.trialstracker.net/) for radicalizing me on the importance the public access to trial data.

I also tried out [GitHub Copilot](https://github.com/features/copilot) while writing this package. It works remarkably well for this task!