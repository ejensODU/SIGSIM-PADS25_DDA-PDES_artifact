import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Set up LaTeX rendering
plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.serif": ["Computer Modern Roman"],
    "text.latex.preamble": r"\usepackage{amsmath}"
})

# Read the data
df = pd.read_csv('PADS_network_simulation_results.csv')

# Create model name mapping
model_name_mapping = {
    'VN2D_grid_network': 'Msh27-2D',
    'VN3D_grid_network': 'Msh9-3D',
    '3D_torus_network': 'Trs9-3D'
}

# Define which sizes to use for each model
model_size_mapping = {
    'VN2D_grid_network': '27_27',
    'VN3D_grid_network': '9_9_9',
    '3D_torus_network': '9_9_9'
}

# Create empty list to store plot data
plot_data = []

# Create figure with appropriate size
plt.figure(figsize=(12, 8))

# Define color cycle and line styles
colors = plt.cm.tab10(np.linspace(0, 1, 10))
line_styles = ['-', '--', ':']
markers = ['o', 's', '^', 'D']

# Define consistent colors for each model class
model_colors = {
    'Msh27-2D': "#4682B4",    # Richer blue (more saturated steelblue)
    'Msh9-3D': "#BC8F8F",    # Deeper pink-brown (more saturated rosybrown)
    'Trs9-3D': "#696969"     # Darker gray (more saturated gray)
}

# Process each model type
lines = []
labels = []

for model in sorted(df['model'].unique()):
    # Only process if the model is in our mapping
    if model in model_size_mapping:
        # Filter data by model and size
        size = model_size_mapping[model]
        model_data = df[(df['model'] == model) & (df['size'] == size)]
        
        # Only continue if we have data
        if model_data.empty:
            continue
            
        base_name = model_name_mapping[model]
        color = model_colors[base_name]

        # Process models with different hop radius values
        for i, hop_radius in enumerate([1, 2, 4]):
            hop_data = model_data[model_data['hop_radius'] == hop_radius]
            if not hop_data.empty:
                mean_data = hop_data.groupby('params_config')['mean_ready_events'].mean()

                # Store data for CSV
                for config, value in mean_data.items():
                    plot_data.append({
                        'model_type': model,
                        'display_name': base_name,
                        'hop_radius': hop_radius,
                        'params_config': config,
                        'mean_ready_events': value
                    })

                line, = plt.plot(mean_data.index, mean_data.values,
                               label=f'{base_name}-{hop_radius}',
                               color=color,
                               linestyle=line_styles[i % len(line_styles)],
                               marker=markers[i % len(markers)],
                               markersize=8,
                               linewidth=2)
                lines.append(line)
                labels.append(f'{base_name}-{hop_radius}H-$C$')

# Create and save the CSV
plot_df = pd.DataFrame(plot_data)
plot_df.to_csv('PADS_plot_data_points_729.csv', index=False)

# Customize the plot
plt.xlabel(r'Delay Distribution Configuration ($C$)', fontsize=28)
plt.ylabel(r'Mean Size $\mathbf{R}$', fontsize=28)

# Apply the font properties to x-axis tick labels
plt.xticks(range(10), [r'$\mathrm{' + str(i) + '}$' for i in range(1, 11)])

# Change both x and y axis label sizes
plt.tick_params(axis='both', labelsize=20)

# Add grid
plt.grid(True, linestyle='--', alpha=1)

# Sort and group labels
labels_sorted = sorted(labels)
msh2d_labels = [l for l in labels_sorted if l.startswith('Msh27-2D')]
msh3d_labels = [l for l in labels_sorted if l.startswith('Msh9-3D')]
trs3d_labels = [l for l in labels_sorted if l.startswith('Trs9-3D')]

# Create corresponding line objects lists
msh2d_lines = [lines[labels.index(l)] for l in msh2d_labels]
msh3d_lines = [lines[labels.index(l)] for l in msh3d_labels]
trs3d_lines = [lines[labels.index(l)] for l in trs3d_labels]

# Create legend entries with empty placeholders for alignment
all_lines = msh2d_lines + msh3d_lines + trs3d_lines
all_labels = [r'\texttt{' + label + '}' for label in msh2d_labels + msh3d_labels + trs3d_labels]

plt.legend(all_lines, all_labels,
          bbox_to_anchor=(0.5, 1.25),
          loc='upper center',
          ncol=3,
          fontsize=20,
          frameon=True,
          columnspacing=1.0)

# Adjust layout to prevent legend cropping
plt.tight_layout()

# Save the plot in both formats
plt.savefig('PADS_mean_REs_729.pdf',
            bbox_inches='tight')

plt.close()