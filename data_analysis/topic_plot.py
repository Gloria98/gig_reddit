import matplotlib
matplotlib.use('Agg')
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import config
from matplotlib.colors import ListedColormap
plt.rcParams.update({'font.size': 18})

def plot_score():
    df = pd.read_csv("topic_opt5.csv", names=['num_topic', 'score'])
    plt.figure(figsize=(9,6))
    plt.xlim(2,13)
    plt.xticks(np.arange(2, 13, step=2))
    plt.plot(df['num_topic'].values, df['score'].values, 'o-',)
    plt.ylabel('Coherence score')
    plt.xlabel('Number of topic')
    plt.grid()
    plt.savefig('topic_opt.png')

# plot the number of post in each topic
def topic_num():
    labels = ['T1: Fair Pay', 'T2: Legal Action', 'T3: Work Incidents', 'T4: Organize Strike', 'T5: Working Time', 'T6: Poor Worker Support']
    nums = []
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    for i in range(6):
        topic = float(i)
        sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
        nums.append(len(sub_posts))
    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots(figsize=(12,6))
    rects1 = ax.barh(x, nums, width,zorder=3)
    ax.set_xlim([0,750])
    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_xlabel('Number of Posts')
    ax.set_ylabel('Topic Number')
    # ax.set_title('Scores by group and gender')
    ax.set_yticks(x)
    ax.set_yticklabels(labels)
    ax.invert_yaxis()
    ax.grid(zorder=0, axis='x')

    def autolabel(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(3, 0),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom')

    # autolabel(rects1)
    plt.tight_layout()
    # ax.legend()
    plt.savefig('topic_num.png')

# plot the percentage of post from each type of work for each topic
def topic_type():
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    type_name = ["Housing/Accommodation", "Caregiving", "Delivery", "Retail", "Passenger Transportation", "Crowd Work", "Education", "Freelance Labor"]
    fig, axs = plt.subplots(2, 3, figsize=(18,9))
    all_type = []
    for i in range(6):
        topic = float(i)
        sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
        sub_total = len(sub_posts)
        type_num = []
        for t in type_name:
            num = 0
            sub_list = config.types[t]
            for sub in sub_list:
                sub_sub_posts = sub_posts[sub_posts['subreddit']==sub]
                num += len(sub_sub_posts)
            type_num.append(100*float(num/sub_total))
        all_type.append(type_num)
    # width = 0.35  # the width of the bars
    y_pos = np.arange(len(type_name))
    x_pos = np.arange(20, 90, 20)
    x_labels = ["20%", "40%", "60%", "80%"]
    axs[0, 0].barh(y_pos, all_type[0])
    axs[0, 0].set_title(f'T1: Fair Pay')
    axs[0, 0].set_yticks(y_pos)
    axs[0, 0].set_yticklabels(type_name)
    axs[0, 0].set_xticks(x_pos)
    axs[0, 0].invert_yaxis()
    axs[0, 1].barh(y_pos, all_type[1])
    axs[0, 1].set_title(f'T2: Legal Action')
    axs[0, 1].invert_yaxis()
    axs[0, 1].sharex(axs[0, 0])
    axs[0, 2].barh(y_pos, all_type[2])
    axs[0, 2].set_title(f'T3: Work Incidents')
    axs[0, 2].invert_yaxis()
    axs[0, 2].sharex(axs[0, 0])
    axs[1, 0].barh(y_pos, all_type[3])
    axs[1, 0].set_title(f'T4: Organize Strike')
    axs[1, 0].set_yticks(y_pos)
    axs[1, 0].set_yticklabels(type_name)
    axs[1, 0].invert_yaxis()
    axs[1, 0].sharex(axs[0, 0])
    axs[1, 1].barh(y_pos, all_type[4])
    axs[1, 1].set_title(f'T5: Working Time')
    axs[1, 1].invert_yaxis()
    axs[1, 1].sharex(axs[0, 0])
    axs[1, 2].barh(y_pos, all_type[5])
    axs[1, 2].set_title(f'T6: Poor Worker Support')
    axs[1, 2].invert_yaxis()
    axs[1, 2].sharex(axs[0, 0])
    axs[0, 0].set_xticklabels(x_labels)
    
    for ax in axs.flat:
        ax.set(xlabel='Percentage of Posts', ylabel='Type of Work')

    # Hide x labels and tick labels for top plots and y ticks for right plots.
    for ax in axs.flat:
        ax.label_outer()
    plt.tight_layout()
    plt.savefig(f'topic_type.png')

# plot the participation patter for each type of work, x is number of comments and y is number of upvotes
def plot_part_all():
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    type_name = ["Housing/Accommodation", "Caregiving", "Delivery", "Retail", "Passenger Transportation", "Crowd Work", "Education", "Freelance Labor"]
    fig, axs = plt.subplots(2, 4, figsize=(18,9))
    i = 0
    for ax in axs.flat:
        sub_list = config.types[type_name[i]]
        df = pd.DataFrame()
        for sub in sub_list:
            sub_posts = all_posts[all_posts['subreddit']==sub]
            df = pd.concat([df, sub_posts], sort=False)
        plot_par(df, ax, type_name[i])
        if i==0:
            ax.legend()
        i+=1
    for ax in axs.flat:
        ax.set(xlabel='Number of Comments', ylabel='Number of Upvotes')

    plt.tight_layout()
    plt.savefig(f'topic_part_type.png')
            
# plot the participation pattern, color code each topic
def plot_par(df, ax, title):
    color_list = ['blue', 'black', 'green', 'purple', 'yellow', 'red']
    topics = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    for i in range(6):
        topic = float(i)
        sub_posts = df[df['Dominant_Topic']==topic]
        x = sub_posts['num_comments'].to_list()
        y = sub_posts['score'].to_list()
        scatter = ax.scatter(x, y, c=color_list[i], alpha=0.5, label=topics[i])
    # ax.legend()
    ax.set_title(title)

# plot the participation pattern of all the posts (not divided between type of work)
def plot_partic():
    # plt.figure(figsize=(9,6))
    fig, ax = plt.subplots(figsize=(9,6))
    color_list = ['blue', 'black', 'green', 'purple', 'yellow', 'red']
    topics = ['T1', 'T2', 'T3', 'T4', 'T5', 'T6']
    all_posts = pd.read_csv("action_ext/post_topic_6_2.csv", lineterminator='\n')
    
    for i in range(6):
        topic = float(i)
        sub_posts = all_posts[all_posts['Dominant_Topic']==topic]
        x = sub_posts['num_comments'].to_list()
        y = sub_posts['score'].to_list()
        scatter = ax.scatter(x, y, c=color_list[i], alpha=0.5, label=topics[i])
    plt.ylabel('Upvotes')
    plt.xlabel('Comments')
    ax.legend()
    plt.savefig('topic_part.png')


plot_part_all()