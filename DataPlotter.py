import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

def save_bar_plot(resolution, y, subfolder, title, y_ticks, x_name = "result", y_name = "amount of occurences", y_min = None, y_max = None):
    fig, ax = plt.subplots()
    x = [i for i, _ in enumerate(resolution)]
    ax.bar(x, y, color=(0.2, 0.8, 0.0, 0.8))
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    ax.set_title(title)
    plt.xticks(x, resolution, rotation = 90)
    plt.yticks(y_ticks)
    if y_min != None:
        axes = plt.gca()
        axes.set_ylim([y_min,y_max])
    fig.set_size_inches(12.8, 9.6)
    fig.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
    plt.close()

def save_pie_plot(labels, amplitude, subfolder, title):
    fig, ax = plt.subplots()
    ax.pie(amplitude, labels = labels, autopct=lambda pct: func(pct, amplitude), startangle=90)
    ax.axis('equal')
    ax.set_title(title)
    fig.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
    plt.close()

def plot_line_chart(data, subfolder, title, figsize, use_interpolation = True):
  plt.figure(figsize=figsize)

  for instance in data:
    if use_interpolation:
      placements_amp = data[instance]
      placements_res = np.array(range(0, len(data[instance])))
      xnew = np.linspace(placements_res.min(), placements_res.max(), 300) 
      spl = make_interp_spline(placements_res, placements_amp, k=3)  # type: BSpline
      power_smooth = spl(xnew)
      plt.plot(xnew, power_smooth, label=instance, linewidth=2)
    else:
      plt.plot(np.array(range(0, len(data[instance]))), data[instance], label=data, linewidth=2)
  plt.legend(loc='best')
  plt.savefig("plots/" + subfolder + "/" + title + ".png", bbox_inches="tight")
  plt.close()


def func(pct, allvals):
    absolute = int(round(pct/100.*np.sum(allvals)))
    return "{:.1f}%\n{:d}".format(pct, absolute)

def dict_to_array(inp_dict):
    keys = [(k) for k,v in inp_dict.items()]
    values = [(v) for k,v in inp_dict.items()]
    return keys, values

def sort_dict(inp_dict): 
    return {k: v for k, v in sorted(inp_dict.items(), key=lambda item: item[1], reverse=True)}

def map_data(input):
  return dict_to_array(sort_dict(input))

def get_y_ticks(amplitude, y_zero = False, min_offset = 0, max_offset = 0):
  y_min = 0
  if not y_zero:
    y_min = min(amplitude)
  return range(y_min + min_offset, max(amplitude) + max_offset)