from numpy.core.fromnumeric import sort
from Definition import Plot_Type
import matplotlib.pyplot as plt


def plot(data, type, values, y_zero = True):
  resolution, amplitude = map_data(data)

  if type == Plot_Type.bar:
    plot_bar_chart(resolution, amplitude, values["subfolder"], values["title"], y_zero)
  #plot_functions[type](data)


def plot_bar_chart(resolution, y, subfolder, title, y_zero, x_name, y_name):
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


def plot_pie_chart(data):
  pass


def plot_line_chart(data):
  pass

def dict_to_array(inp_dict):
    keys = [(k) for k,v in inp_dict.items()]
    values = [(v) for k,v in inp_dict.items()]
    return keys, values

def sort_dict(inp_dict): 
    return {k: v for k, v in sorted(inp_dict.items(), key=lambda item: item[1], reverse=True)}

def map_data(input):
  return dict_to_array(sort_dict(input))