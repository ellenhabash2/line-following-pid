#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyArrow
import csv


def read_path_data(filename):
    time_data = []
    x_data = []
    y_data = []
    theta_data = []
    light_data = []
    distance_data = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            time_data.append(float(row['Time']))
            x_data.append(float(row['X']))
            y_data.append(float(row['Y']))
            theta_data.append(float(row['Theta']))
            light_data.append(int(row['Light']))
            distance_data.append(int(row['Dist']))

    return {
        'time': np.array(time_data),
        'x': np.array(x_data),
        'y': np.array(y_data),
        'theta': np.array(theta_data),
        'light': np.array(light_data),
        'distance': np.array(distance_data)
    }


def plot_robot_path(data, save_figure=True):
    fig = plt.figure(figsize=(16, 10))

    ax1 = plt.subplot(2, 3, 1)
    ax1.plot(data['x'], data['y'], 'b-', linewidth=2, label='Robot Path')
    ax1.plot(data['x'][0], data['y'][0], 'go', markersize=12, label='Start')
    ax1.plot(data['x'][-1], data['y'][-1], 'ro', markersize=12, label='End')

    skip = max(1, len(data['x']) // 15)
    for i in range(0, len(data['x']), skip):
        theta_rad = np.deg2rad(data['theta'][i] / 100.0)
        dx = 3 * np.cos(theta_rad)
        dy = 3 * np.sin(theta_rad)
        ax1.arrow(data['x'][i], data['y'][i], dx, dy,
                  head_width=2, head_length=1.5, fc='red', ec='red', alpha=0.6)

    ax1.set_xlabel('X Position (cm)', fontsize=12)
    ax1.set_ylabel('Y Position (cm)', fontsize=12)
    ax1.set_title('Robot Path with Orientation', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axis('equal')

    ax2 = plt.subplot(2, 3, 2)
    scatter = ax2.scatter(data['x'], data['y'], c=data['light'],
                          cmap='RdYlGn_r', s=50, alpha=0.7)
    ax2.plot(data['x'][0], data['y'][0], 'go', markersize=12, label='Start')
    ax2.plot(data['x'][-1], data['y'][-1], 'ro', markersize=12, label='End')

    plt.colorbar(scatter, ax=ax2, label='Light Sensor Value')
    ax2.set_xlabel('X Position (cm)', fontsize=12)
    ax2.set_ylabel('Y Position (cm)', fontsize=12)
    ax2.set_title('Path with Light Sensor Data', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.axis('equal')

    ax3 = plt.subplot(2, 3, 3)
    dark_threshold = 45
    dark_points_x = data['x'][data['light'] < dark_threshold]
    dark_points_y = data['y'][data['light'] < dark_threshold]

    ax3.plot(data['x'], data['y'], 'b-', linewidth=1, alpha=0.3, label='Full Path')
    if len(dark_points_x) > 0:
        ax3.scatter(dark_points_x, dark_points_y, c='black', s=80,
                    label='Black Line Position', marker='s', alpha=0.8)

    ax3.plot(data['x'][0], data['y'][0], 'go', markersize=12, label='Start')
    ax3.plot(data['x'][-1], data['y'][-1], 'ro', markersize=12, label='End')

    ax3.set_xlabel('X Position (cm)', fontsize=12)
    ax3.set_ylabel('Y Position (cm)', fontsize=12)
    ax3.set_title('Estimated Black Line Shape (BONUS)', fontsize=14, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.axis('equal')

    ax4 = plt.subplot(2, 3, 4)
    time_sec = data['time'] / 1000.0
    ax4.plot(time_sec, data['theta'] / 100.0, 'purple', linewidth=2)
    ax4.set_xlabel('Time (seconds)', fontsize=12)
    ax4.set_ylabel('Orientation (degrees)', fontsize=12)
    ax4.set_title('Robot Orientation vs Time', fontsize=12, fontweight='bold')
    ax4.grid(True, alpha=0.3)

    ax5 = plt.subplot(2, 3, 5)
    ax5_twin = ax5.twinx()

    line1 = ax5.plot(time_sec, data['light'], 'orange', linewidth=2, label='Light Sensor')
    line2 = ax5_twin.plot(time_sec, data['distance'], 'cyan', linewidth=2, label='Distance Sensor')

    ax5.set_xlabel('Time (seconds)', fontsize=12)
    ax5.set_ylabel('Light Sensor Value', fontsize=12, color='orange')
    ax5_twin.set_ylabel('Distance (cm)', fontsize=12, color='cyan')
    ax5.tick_params(axis='y', labelcolor='orange')
    ax5_twin.tick_params(axis='y', labelcolor='cyan')

    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax5.legend(lines, labels, loc='upper right')
    ax5.set_title('Sensor Readings vs Time', fontsize=12, fontweight='bold')
    ax5.grid(True, alpha=0.3)

    ax6 = plt.subplot(2, 3, 6)
    ax6.axis('off')

    dx = np.diff(data['x'])
    dy = np.diff(data['y'])
    distances = np.sqrt(dx ** 2 + dy ** 2)
    total_distance = np.sum(distances)
    total_time = (data['time'][-1] - data['time'][0]) / 1000.0
    avg_speed = total_distance / total_time if total_time > 0 else 0

    stats_text = f"""
    Path Statistics
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    Data Points: {len(data['x'])}

    Total Distance: {total_distance:.1f} cm

    Total Time: {total_time:.1f} seconds

    Average Speed: {avg_speed:.1f} cm/s

    X Range: {np.min(data['x']):.1f} to {np.max(data['x']):.1f} cm

    Y Range: {np.min(data['y']):.1f} to {np.max(data['y']):.1f} cm

    Average Light: {np.mean(data['light']):.1f}

    Final Distance: {data['distance'][-1]} cm
    """

    ax6.text(0.1, 0.5, stats_text, fontsize=11, family='monospace',
             verticalalignment='center', bbox=dict(boxstyle='round',
                                                   facecolor='wheat', alpha=0.5))

    plt.suptitle('Robot Odometry Analysis',
                 fontsize=16, fontweight='bold', y=0.98)
    plt.tight_layout()

    if save_figure:
        plt.savefig('robot_path_analysis.png', dpi=300, bbox_inches='tight')
        print("Image saved: robot_path_analysis.png")

    plt.show()


def plot_simple_path(data, save_figure=True):
    plt.figure(figsize=(10, 10))

    plt.plot(data['x'], data['y'], 'b-', linewidth=3)
    plt.plot(data['x'][0], data['y'][0], 'go', markersize=15, label='Start')
    plt.plot(data['x'][-1], data['y'][-1], 'ro', markersize=15, label='End')

    skip = max(1, len(data['x']) // 10)
    for i in range(0, len(data['x']), skip):
        theta_rad = np.deg2rad(data['theta'][i] / 100.0)
        dx = 4 * np.cos(theta_rad)
        dy = 4 * np.sin(theta_rad)
        plt.arrow(data['x'][i], data['y'][i], dx, dy,
                  head_width=3, head_length=2, fc='red', ec='red', alpha=0.7)

    plt.xlabel('X Position (cm)', fontsize=14)
    plt.ylabel('Y Position (cm)', fontsize=14)
    plt.title('Robot Path', fontsize=16, fontweight='bold')
    plt.legend(fontsize=12)
    plt.grid(True, alpha=0.4)
    plt.axis('equal')

    if save_figure:
        plt.savefig('robot_path_simple.png', dpi=300, bbox_inches='tight')
        print("Image saved: robot_path_simple.png")

    plt.show()


def main():
    print("=" * 60)
    print("Robot Path Visualization")
    print("=" * 60)

    filename = input("\nEnter filename (default: path.txt): ").strip()
    if not filename:
        filename = 'path.txt'

    try:
        print(f"\nReading file: {filename}")
        data = read_path_data(filename)
        print(f"Read {len(data['x'])} data points")

        print("\nBasic Information:")
        print(f"   - X Range: {np.min(data['x']):.1f} to {np.max(data['x']):.1f} cm")
        print(f"   - Y Range: {np.min(data['y']):.1f} to {np.max(data['y']):.1f} cm")
        print(f"   - Total Time: {(data['time'][-1] - data['time'][0]) / 1000:.1f} seconds")

        print("\nGenerating full analysis plot...")
        plot_robot_path(data, save_figure=True)

        choice = input("\nDo you want a simple plot too? (y/n): ").strip().lower()
        if choice == 'y' or choice == 'yes':
            print("\nGenerating simple path plot...")
            plot_simple_path(data, save_figure=True)

        print("\nCompleted successfully!")
        print("=" * 60)

    except FileNotFoundError:
        print(f"\nError: File '{filename}' not found!")
        print("Make sure the file exists in the same directory.")
    except Exception as e:
        print(f"\nError occurred: {e}")


if __name__ == "__main__":
    main()