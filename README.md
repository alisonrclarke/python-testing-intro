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

You can install the package using your favourite package manager, whether that's poetry, pipenv, pip, conda or something else. I'm going to use poetry. As I don't currently have any dependencies I'll run `poetry init`, accepting default values for everything, but not adding dependencies yet:

```bash
$ poetry init
```

That creates a `pyproject.toml` file containing details of our project.

Now we can install `pytest`, adding it as a dev dependency because it's not needed by people who will run our code, just by people developing it:

```bash
poetry add --dev pytest
```

We can now open a shell in a poetry environment to run our code as before:

```bash
$ poetry shell
(python-testing-intro-EqBKcORj-py3.7) bash-3.2$ python main.py 9
Data: [53, 86, 60, 13, 40, 59, 71, 83, 10]
Working...
Grid:
53	86	60
13	40	59
71	83	10
```

(If you don't use poetry or already have an environment set up, just use `pip install pytest` or `conda install pytest` in your environment.)
