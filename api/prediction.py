import torch
import numpy as np
import pickle
from torch.autograd import Variable
from tqdm import tqdm_notebook as tqdm

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

class MatrixFactorization(torch.nn.Module):
    def __init__(self, n_users, n_items, n_factors=20):
        super().__init__()
        # create user embeddings
        self.user_factors = torch.nn.Embedding(n_users, n_factors) # think of this as a lookup table for the input.
        # create item embeddings
        self.item_factors = torch.nn.Embedding(n_items, n_factors) # think of this as a lookup table for the input.
        self.user_factors.weight.data.uniform_(0, 0.05)
        self.item_factors.weight.data.uniform_(0, 0.05)
        
    def forward(self, data):
        # matrix multiplication
        users, items = data[:,0], data[:,1]
        return (self.user_factors(users)*self.item_factors(items)).sum(1)

    
    def predict(self, users, items):
      if isinstance(users, list):
        users = torch.tensor([users], device=device)
      if isinstance(items, list):
        items = torch.tensor([items], device=device)
    
      # Ensure the indices are within range
      if users.max() >= self.user_factors.num_embeddings or items.max() >= self.item_factors.num_embeddings:
          raise ValueError("User or item index out of bounds.")
      
      # Stack users and items together
      
      data = torch.stack((users, items), dim=1)  # Shape (N, 2)

      if torch.cuda.is_available():
          data = data.cuda()  # Move to GPU if necessary

      return self.forward(data)
  
  
def load_model():
    
    # Define the same model structure
    n_users = 100000  # Replace with actual number of users
    n_items = 29492  # Replace with actual number of items
    n_factors = 8

    
    # Load the model
    model = MatrixFactorization(n_users, n_items, n_factors).to(device)
    model.load_state_dict(torch.load("api/model.pth", map_location=device))
    model.eval()

    # Ensure inputs are on the correct device


    # Load the mappings
    with open("api/mappings.pkl", "rb") as f:
        mappings = pickle.load(f)

    userid2idx = mappings["userid2idx"]
    movieid2idx = mappings["history2idx"]
    idx2userid = mappings["idx2userid"]
    idx2movieid = mappings["idx2history"]
    return model