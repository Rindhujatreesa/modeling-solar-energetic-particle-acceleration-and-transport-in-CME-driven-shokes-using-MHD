import torch
import torch.nn as nn
import numpy as np

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
    """Trains the network using a Masked Mean Squared Error (M-MSE) loss function.
    
    Args:
        model: PADReconstructionNet model
        corrupted_data: Input data with masked values (NxD array)
        target_data: Ground truth data (NxD array)
        mask: Binary mask where 1 indicates missing/corrupted values (NxD array)
        epochs: Number of training iterations
        lr: Learning rate
    
    Returns:
        losses: List of loss values per epoch for monitoring training convergence
    
    The model is trained to impute only the masked positions (~M), 
    while leaving corrupted non-masked data unchanged.
    """
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    criterion = nn.MSELoss()
    
    X = torch.tensor(corrupted_data, dtype=torch.float32)
    Y = torch.tensor(target_data, dtype=torch.float32)
    M = torch.tensor(mask, dtype=torch.float32)
    
    losses = []
    
    for epoch in range(epochs):
        model.train()
        optimizer.zero_grad()
        
        predictions = model(X)
        # Compute loss exclusively over missing values to guide reconstruction profile
        loss = criterion(predictions * (~M.bool()).float(), Y * (~M.bool()).float())
        
        loss.backward()
        optimizer.step()
        
        losses.append(loss.item())
        
        # Print progress every 50 epochs
        if (epoch + 1) % 50 == 0:
            print(f"Epoch {epoch + 1}/{epochs} - Loss: {loss.item():.6f}")
    
    print(f"Training complete! Final loss: {losses[-1]:.6f}")
    return losses


def impute_corrupted_data(model, corrupted_data, mask):
    """
    Imputes missing values in corrupted data while preserving non-masked data points.
    
    Args:
        model: Trained PADReconstructionNet model
        corrupted_data: Input data with masked values (NxD array or tensor)
        mask: Binary mask where True indicates AVAILABLE data, False indicates MISSING data
    
    Returns:
        Numpy array with the same shape as corrupted_data, where:
        - Available positions (mask == True) preserve original corrupted values
        - Missing positions (mask == False) are filled with model predictions
    """
    model.eval()
    
    with torch.no_grad():
        X = torch.tensor(corrupted_data, dtype=torch.float32) if not isinstance(corrupted_data, torch.Tensor) else corrupted_data
        M = torch.tensor(mask, dtype=torch.float32) if not isinstance(mask, torch.Tensor) else mask
        
        # Get model predictions for all positions
        predictions = model(X)
        
        # Blend: keep original values where mask == True (available), 
        # use predictions where mask == False (missing)
        imputed = corrupted_data.copy() if hasattr(corrupted_data, 'copy') else X.clone()
        imputed = torch.tensor(imputed, dtype=torch.float32) if not isinstance(imputed, torch.Tensor) else imputed
        
        # Replace only missing positions with predictions
        # M = True (available) -> keep original, M = False (missing) -> use predictions
        imputed = M * imputed + (1 - M) * predictions
        
        # Convert to numpy if input was numpy
        if isinstance(corrupted_data, np.ndarray):
            return imputed.detach().cpu().numpy()
        return imputed