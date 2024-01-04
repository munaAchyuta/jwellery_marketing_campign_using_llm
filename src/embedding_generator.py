import numpy as np
import torch
torch.manual_seed(45)
from sentence_transformers import models as st_models
from sentence_transformers import SentenceTransformer, util
from torch import nn
from transformers import pipeline

def get_embedding_model(model_name=None):
    if model_name is None:
        model_name = 'all-MiniLM-L6-v2'
    model = SentenceTransformer(model_name)

    return model