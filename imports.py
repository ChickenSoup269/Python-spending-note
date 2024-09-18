import inquirer #
import json #
import requests #
import os #
import uuid #
import termcharts #
import pyfiglet #
import random #
import re #
import sys #
import time #
import keyboard #
import termcharts.bar_chart
# =================================
from datetime import datetime, timedelta
from tabulate import tabulate
from collections import defaultdict
from colorama import Fore, Back, Style, init
from unidecode import unidecode 
# ================================
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
# import các hàm chung
from utils import *
#  =================================
# Font chữ animation
from terminaltexteffects.effects.effect_rain import Rain
from terminaltexteffects.effects.effect_blackhole import Blackhole
from terminaltexteffects.effects.effect_beams import Beams
from terminaltexteffects.effects.effect_print import Print
from terminaltexteffects.effects.effect_scattered import Scattered
from terminaltexteffects.effects.effect_burn import Burn
# from terminaltexteffects.effects.effect_binarypath import BinaryPath
