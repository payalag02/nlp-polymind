"""
Starting project
"""

import hydra
from omegaconf import DictConfig
from src.agent.expert import Expert
from src.agent.team import ExpertTeam
from src.agent.critic import Critic
from src.data import Data
from src.eval import Debate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@hydra.main(version_base=None, config_path="configs", config_name="config.yaml")
def main(config: DictConfig):
    """
    Loads the config and runs the experiment.
    """
    data = Data(config)
    dataset = data.get_tokenized_data()
    train_data = dataset["train"]
    eval_data = dataset["validation"]
    test_data = dataset["test"]

    logger.debug(f"Train data size: {len(train_data)}")
    logger.debug(f"Eval data size: {len(eval_data)}")
    logger.debug(f"Test data size: {len(test_data)}")

    expert = Expert(config, 0, train_data, eval_data)
    expert.fine_tune_std_lora(save=False)

    truncated_eval_data = eval_data.select(range(5))
    truncated_test_data = test_data.select(range(5))


    for task_set in truncated_eval_data:
        task = task_set["dialogue"]
        ground_truth = task_set["summary"]
        answer = expert.generate(task)
        logger.info(f"Task: {task}")
        logger.info(f"Ground truth: {ground_truth}")
        logger.info(f"Answer: {answer}")


if __name__ == "__main__":
    main()