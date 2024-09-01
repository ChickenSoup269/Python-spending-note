import inquirer #
import json #
import requests #
import os #
import uuid #
import termcharts #
import pyfiglet #
import random #
import termcharts.bar_chart
from datetime import datetime, timedelta
from tabulate import tabulate
from collections import defaultdict
from colorama import Fore, Back, Style, init
# 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
#  =================================
from utils import *

# tính giờ để chào sáng, chiều ,tối
current_time = datetime.now()
dt_string = current_time.strftime("%H:%M:%S")
current_hour = current_time.hour