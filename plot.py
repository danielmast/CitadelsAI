from stable_baselines3.common import results_plotter

log_dir = "/Users/daniel/repos/CitadelsAI/logs"
# results_plotter.plot_results([log_dir], 1e5, results_plotter.X_TIMESTEPS, "CitadelsAI")
results_plotter.plot_results([log_dir], num_timesteps=200000, x_axis=results_plotter.X_TIMESTEPS, task_name="CitadelsAI")
print('debug')
