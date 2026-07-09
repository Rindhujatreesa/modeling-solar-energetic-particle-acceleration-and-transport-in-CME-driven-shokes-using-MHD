import torch
import torch.nn as nn

class PADReconstructionNet(nn.Module):
    """
    Physics-inspired Deep Autoencoder architecture designed to fill structural
    observation gaps in spacecraft particle pitch-angle tracking systems.
    """
    def __init__(self, input_dim):
        super().__init__()
        # Encoder profiles the partial distribution shape
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.Tanh(), # Tanh maintains clean wave gradients for fluid profiles
            nn.Linear(64, 16),
            nn.Tanh()
        )
        # Decoder reconstructs the smooth, physical underlying continuum
        self.decoder = nn.Sequential(
            nn.Linear(16, 64),
            nn.Tanh(),
            nn.Linear(64, input_dim),
            nn.ReLU() # Particle distributions remain strictly non-negative
        )
        
    def forward(self, x):
        latent = self.encoder(x)
        reconstruction = self.decoder(latent)
        return reconstruction

def train_reconstructor(model, corrupted_data, target_data, mask, epochs=200, lr=1e-3):
    """Trains the network using a Masked Mean Squared Error (M-MSE) loss function"""
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    X = torch.tensor(corrupted_data, dtype=torch.float32)
    Y = torch.tensor(target_data, dtype=torch.float32)
    M = torch.tensor(mask, dtype=torch.float32)
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        predictions = model(X)
        # Compute loss exclusively over missing values to guide reconstruction profile
        loss = criterion(predictions * (~M.bool()).float(), Y * (~M.bool()).float())
        
        loss.backward()
        optimizer.step()