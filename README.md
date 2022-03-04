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
