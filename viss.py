import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def first_plot():
    all_points = []

    def on_click(event):
        if float(event.xdata) is not None and float(event.ydata) is not None:
            # Add point to the list
            all_points.append((float(event.xdata), float(event.ydata)))
            print(f"Point added: ({float(event.xdata):.2f}, {float(event.ydata):.2f})")

            # Plot the point
            plt.plot(float(event.xdata), float(event.ydata), 'ro')  # 'ro' for red circles
            plt.draw()

    # Create the first plot
    fig, ax = plt.subplots()
    ax.set_title("Click to add points (Close when done)")
    ax.set_xlim(0, 10)  # Customize the range as needed
    ax.set_ylim(0, 10)

    # Connect click event
    fig.canvas.mpl_connect('button_press_event', on_click)

    # Show the first plot
    plt.show()
    return all_points

def second_plot(all_points):
    rect_points = []  # Store rectangle points

    def on_click(event):
        nonlocal rect_points
        if float(event.xdata) is not None and float(event.ydata) is not None:
            # Add the clicked point to the rectangle points
            rect_points.append((float(event.xdata), float(event.ydata)))
            print(f"Rectangle Point added: ({float(event.xdata):.2f}, {float(event.ydata):.2f})")

            # Plot the point
            plt.plot(float(event.xdata), float(event.ydata), 'bo')  # 'bo' for blue circles
            plt.draw()

            # If 4 points are selected, draw the rectangle
            if len(rect_points) == 4:
                draw_rectangle(rect_points)

    def draw_rectangle(rect_points):
        x_coords = [p[0] for p in rect_points]
        y_coords = [p[1] for p in rect_points]
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # Add the rectangle to the plot
        rect = Rectangle((x_min, y_min), x_max - x_min, y_max - y_min,
                         linewidth=2, edgecolor='green', facecolor='none')
        ax.add_patch(rect)
        plt.draw()

        # Disconnect the click event to finalize the rectangle
        fig.canvas.mpl_disconnect(cid)
        print("Rectangle complete! Closing plot...")
        save_plot_and_points(rect_points)
        plt.pause(2)
        plt.close()

    def save_plot_and_points(rect_points):
        # Save all points and rectangle points to a file
        with open("points_and_rectangle.txt", "w") as file:
            file.write("All Points:\n")
            for point in all_points:
                file.write(f"{point}\n")
            file.write("\nRectangle Points:\n")
            for point in rect_points:
                file.write(f"{point}\n")
        print("Points saved to 'points_and_rectangle.txt'")

        # Save the final plot as an image
        plt.savefig("final_plot.png")
        print("Plot saved as 'final_plot.png'")

    # Create the second plot
    fig, ax = plt.subplots()
    ax.set_title("Select 4 points for the rectangle (Close when done)")
    ax.set_xlim(0, 10)  # Customize the range as needed
    ax.set_ylim(0, 10)

    # Plot the points from the first plot
    for point in all_points:
        plt.plot(point[0], point[1], 'ro')  # 'ro' for red circles

    # Connect click event
    cid = fig.canvas.mpl_connect('button_press_event', on_click)

    # Show the second plot
    plt.show()

    x_coords = [p[0] for p in rect_points]
    y_coords = [p[1] for p in rect_points]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)

    return x_min, x_max, y_min, y_max


def collect():
    points = first_plot()
    rect_points = second_plot(points)

    return points, rect_points

