import seaborn as sns
color_zoo = sns.color_palette("Blues")
colors = {
    "ours": color_zoo[-1],
    "baseline1": color_zoo[3],
    "baseline2": color_zoo[2],
    "baseline3": color_zoo[1]
}