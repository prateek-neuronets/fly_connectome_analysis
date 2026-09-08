import powerlaw
import matplotlib.pyplot as plt

def plot_degree_distribution(degrees):
    fit = powerlaw.Fit(degrees, discrete=True)

    fig, ax = plt.subplots(figsize=(10, 10), dpi=1000)

    fit.plot_pdf(
        color='red', markersize=15, marker='o', linestyle='',
        label='Fitted Data', original_data=False, ax=ax
    )
    fit.plot_pdf(
        color='black', markersize=15, marker='o', linestyle='',
        label='Empirical Data', original_data=True, ax=ax
    )
    fit.power_law.plot_pdf(
        color='darkblue', linewidth=3, label='fitted curve', ax=ax
    )

    ax.set_xlabel('$k$', fontsize=40)
    ax.set_ylabel('P(k)', fontsize=40)
    ax.tick_params(labelsize=40, length=10, width=2, pad=15)

    ax.legend(
        fontsize=30,
        bbox_to_anchor=(0.25, 0.25, 0.40, 0.05),
        frameon=False
    )

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.show()

    return fit
