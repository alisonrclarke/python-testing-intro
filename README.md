# python-testing-intro: Writing tests to save time

This repo holds the code for a demo session to be held at the [SSI Collaborations Workshop 2022](https://www.software.ac.uk/cw22).

Writing automated tests for research software can sometimes feel like something that will slow you down. This demo will show how you can use tests as a tool to save you time as you write your code, as well as giving you greater confidence in the results. If you’ve never written a unit test before, or have tried in the past but given up, this demo aims to get you going and to use automated tests in a way that helps you and suits your project.

The demo will show:
* how to extract part of a section of code into a function to enable easier testing (as well as making your code clearer!)
* how to add unit tests to quickly check that the function works correctly with different input values
* how to use continuous integration to run your tests on every push, to ensure your software still works even when other changes are made

The demo will use python and pytest (though the principles could be applied to other programming languages), and will use GitHub Actions for continuous integration.

## Initial code

Our starting point is a simple script which generates 16 random numbers and lays them out in a grid:

https://github.com/alisonrclarke/python-testing-intro/blob/7c817c468278965a46bb893888eb7f599f7288f9/main.py#L1-L25

Let's imagine the code is a bit more complex, doing some calculations that take a few seconds to run: we use `time.sleep` to mimic this.

Here's what it looks like when you run it:

```bash
$ python main.py
Data: [98, 54, 83, 35, 55, 58, 21, 33, 37, 67, 59, 46, 34, 65, 30, 10]
Working...
Grid:
98	54	83	35
55	58	21	33
37	67	59	46
34	65	30	10
```

## Varying the data size

Now let's imagine we need to allow the user to determine the size of the data. We use `sys.argv` to get a value from the command line and use that to generate the list of values.

https://github.com/alisonrclarke/python-testing-intro/blob/629d94d2ce69bfbacef3171c0727ac5effc404a3/main.py#L6-L11

(We should ideally check that the user has provided a valid integer and give them an appropriate error message if not, but I'll leave that as an exercise to the reader.)

We then need to determine the grid size from the data size. We want the grid to be square, so as a starting point let's use the square root of `data_size`, using `int` to round it down:

https://github.com/alisonrclarke/python-testing-intro/blob/629d94d2ce69bfbacef3171c0727ac5effc404a3/main.py#L15

We then use `grid_size` as the limit when populating our grid:

https://github.com/alisonrclarke/python-testing-intro/blob/629d94d2ce69bfbacef3171c0727ac5effc404a3/main.py#L18-L23

And we can run it to create different sizes of grid:

```bash
$ python main.py 9
Data: [70, 32, 72, 66, 61, 71, 87, 79, 38]
Working...
Grid:
70	32	72
66	61	71
87	79	38
```

```bash
$ python main.py 16
Data: [15, 22, 2, 51, 85, 62, 3, 91, 75, 54, 82, 89, 56, 97, 14, 43]
Working...
Grid:
15	22	2	51
85	62	3	91
75	54	82	89
56	97	14	43
```

But what happens if we try it with a non-square number?

```bash
python main.py 8
Data: [93, 81, 59, 71, 19, 65, 4, 72]
Working...
Grid:
93	81
59	71
```

Rounding down the grid size isn't working: we're not putting all of our data into the grid. And because of our "complex calculation", trying out different options takes a long time. Wouldn't it be great if we could just try out the part of the code that calculates the grid size, with different options? Automated tests can help us!

## Testing preparation

When we write our test we will want to keep it apart from the rest of the code, so we'll put it in a new file. From that new file we'll need to import our current **main.py** file. But if we do that currently, it will run all of the code on import, including the parts that take a long time. So the first thing we need to do is to put our current code into a function:

https://github.com/alisonrclarke/python-testing-intro/blob/bb57a5b24de65ea633f812b567a25c3c34019a2b/main.py#L7-L12

(The rest of our code is also indented now.)

We then add this 'magic' idiom at the bottom of the file:

https://github.com/alisonrclarke/python-testing-intro/blob/bb57a5b24de65ea633f812b567a25c3c34019a2b/main.py#L39-L41

What this does is to call the `main` function whenever the file is run from the command line, so the behaviour will be as it was before.

We should also put the code we want to test in a new function:

https://github.com/alisonrclarke/python-testing-intro/blob/30ab21f9afcf0ad1393ab1b7293d975359756087/main.py#L7-L9

And then we call our function from `main.py`:

https://github.com/alisonrclarke/python-testing-intro/blob/30ab21f9afcf0ad1393ab1b7293d975359756087/main.py#L23

You can check that this works as before.

## Installing pytest

The next thing we need to do is to install the `pytest` package. Python does come with a built-in testing framework, `unittest`, but `pytest` can be easier to use.

You can install the package using your favourite package manager, whether that's pipenv, pip, conda, poetry or something else. I'm going to use pipenv.

I'm installing `pytest` as a dev dependency because it's not needed by people who will run our code, just by people developing it:

```
$ pipenv install pytest
Creating a virtualenv for this project...
Pipfile: /Users/ksvf48/Documents/dev/python-testing-intro/Pipfile
Using /usr/local/opt/python/libexec/bin/python (3.9.12) to create virtualenv...
⠹ Creating virtual environment...created virtual environment CPython3.9.12.final.0-64 in 1584ms
  creator CPython3Posix(dest=/Users/ksvf48/.virtualenvs/python-testing-intro-mUyCU3bK, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/Users/ksvf48/Library/Application Support/virtualenv)
    added seed packages: pip==22.0.4, setuptools==61.0.0, wheel==0.37.1
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator

✔ Successfully created virtual environment!
Virtualenv location: /Users/ksvf48/.virtualenvs/python-testing-intro-mUyCU3bK
Creating a Pipfile for this project...
Installing pytest...
Adding pytest to Pipfile's [packages]...
✔ Installation Succeeded
Pipfile.lock not found, creating...
Locking [dev-packages] dependencies...
Locking [packages] dependencies...
Building requirements...
Resolving dependencies...
✔ Success!
Updated Pipfile.lock (1ffa2d)!
Installing dependencies from Pipfile.lock (1ffa2d)...
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 0/0 — 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

That creates files `Pipfile` and `Pipfile.lock` containing our dependencies.

We can now open a shell in the virtualenv created by pipenv, to run our code as before:

```bash
$ pipenv shell
Launching subshell in virtual environment...
...
(python-testing-intro) bash-3.2$ python main.py 9
Data: [53, 86, 60, 13, 40, 59, 71, 83, 10]
Working...
Grid:
53	86	60
13	40	59
71	83	10
```

(If you don't use pipenv or already have an environment set up, just use `poetry install pytest`, `pip install pytest` or `conda install pytest` in your environment.)

## First test

We now create a file `main_test.py` with the following contents:

https://github.com/alisonrclarke/python-testing-intro/blob/ba85d4e80efab4fb997aed4736f6c14a58242cca/main_test.py#L1-L5

`pytest` will find any file named `test_*.py` or `*_test.py` and run any functions with names starting `test_`. So here, we import our function from `main.py`, then use `assert`, which will raise an error if what follows does not evaluate to `True`, e.g. bool `False`, non-zero values, values that are not None. So we assert that the value returned by `get_grid_size` will be 3 when called with value 9, and 4 when called with value 16.

We run the test as follows:

```
$ pytest
============================ test session starts =============================
platform darwin -- Python 3.7.8, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/ksvf48/Documents/dev/python-testing-intro
collected 1 item                                                             

main_test.py .                                                         [100%]

============================= 1 passed in 0.01s ==============================
```

`pytest` has found our test in `main_test.py` and run it, and tells us the test passed. And in 0.01s - must faster than waiting for our "complex function" to run!

## Parameterising tests

We need to add some more test cases, for example non-square numbers. You might have noticed that we had to copy and paste some code earlier to try our function with two different values. `pytest` offers a better way to repeat tests like this: another way to save you time!

https://github.com/alisonrclarke/python-testing-intro/blob/ac96872cf961cda3bd1e724567a6fbb1d8856dcd/main_test.py#L1-L11

We first define an array with our test values as tuples, so in our case the first value is the parameter, and the second is the expected output from `get_grid_size`. Then we use the decorator `@pytest.mark.parametrize("data_size,expected", grid_size_data)` at the top of our function. Don't worry if you're unfamiliar with decorators: for now you just need to know that this decorator will mean that pytest calls the function once for each tuple in `grid_size_data` and passes the tuple as arguments to the function.

So we modify the function to accept the arguments we defined (`data_size` and `expected`) and use them to call `get_grid_size` and check the output.

 Now when we run `pytest` we see:

 ```
 $ pytest
============================ test session starts =============================
platform darwin -- Python 3.7.8, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/ksvf48/Documents/dev/python-testing-intro
collected 2 items                                                            

main_test.py ..                                                        [100%]

============================= 2 passed in 0.01s ==============================
```

`pytest` has now run two tests, i.e. it has repeated the test with both of our sets of values.

So far our tests have passed. But remember when we tried passing a non-square number? Let's add some extra cases to our parameterised tests:

https://github.com/alisonrclarke/python-testing-intro/blob/1bf5764debbc49d07d01fa15e238df636c1867d9/main_test.py#L4-L9

Now two of our tests fail:

```
$ pytest
============================ test session starts =============================
platform darwin -- Python 3.7.8, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/ksvf48/Documents/dev/python-testing-intro
collected 4 items                                                            

main_test.py ..FF                                                      [100%]

================================== FAILURES ==================================
__________________________ test_get_grid_size[10-4] __________________________

data_size = 10, expected = 4

    @pytest.mark.parametrize("data_size,expected", grid_size_data)
    def test_get_grid_size(data_size, expected):
>       assert get_grid_size(data_size) == expected
E       assert 3 == 4
E        +  where 3 = get_grid_size(10)

main_test.py:13: AssertionError
__________________________ test_get_grid_size[15-4] __________________________

data_size = 15, expected = 4

    @pytest.mark.parametrize("data_size,expected", grid_size_data)
    def test_get_grid_size(data_size, expected):
>       assert get_grid_size(data_size) == expected
E       assert 3 == 4
E        +  where 3 = get_grid_size(15)

main_test.py:13: AssertionError
========================== short test summary info ===========================
FAILED main_test.py::test_get_grid_size[10-4] - assert 3 == 4
FAILED main_test.py::test_get_grid_size[15-4] - assert 3 == 4
======================== 2 failed, 2 passed in 0.04s =========================
```

So we've shown that our function isn't behaving as we'd like - now let's fix it. In this case we just want to alter the code so that it uses the `math.ceil` function to return the nearest integer greater than or equal to the square root:

https://github.com/alisonrclarke/python-testing-intro/blob/1bf5764debbc49d07d01fa15e238df636c1867d9/main.py#L7-L9

And our tests now pass:

```
$ pytest
============================ test session starts =============================
platform darwin -- Python 3.7.8, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/ksvf48/Documents/dev/python-testing-intro
collected 4 items                                                            

main_test.py ....                                                      [100%]

============================= 4 passed in 0.01s ==============================
```

We might want to add further test cases, like 0, negative numbers, very large numbers etc. But the good news is if we did do that they would take barely any additional time to run. All our test cases would probably run in well under a second - that's a lot quicker than waiting for our code to run, and typing in the parameters on the command line, and hoping you don't miss a case.
