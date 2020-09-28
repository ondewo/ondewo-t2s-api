from typing import Dict, List, Any
import numpy as np
import torch

from inference.melgan_core import Generator


class MelGAN():
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model = Generator(self.config["input_size"], self.config["ngf"], self.config["n_residual_layers"]).to(self.config["device"])
        self.model.load_state_dict(torch.load(self.config["load_path"], map_location=self.config["device"]))

    def synthesize(self, mels: List[np.ndarray]) -> List[np.ndarray]:
        mels_tensor = torch.from_numpy(np.array(mels))
        with torch.no_grad():
            preds = self.model(mels_tensor.to(self.config["device"])).squeeze(1)
        
        result: List[np.ndarray] = [pred.cpu().numpy() for pred in preds]
        return result