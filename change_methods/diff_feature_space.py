import torch
import torchvision.models as models
import torch.nn as nn
import torch.nn.functional as F
from torchvision.models import MobileNet_V3_Small_Weights


class DiffFeatureSpace:
    def __init__(self, threshold):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.threshold = threshold
        self.model = models.mobilenet_v3_small(weights=MobileNet_V3_Small_Weights.DEFAULT).to(self.device)
        self.model.eval()
        self.feature_extractor = self.model.features.to(self.device)

    def forward(self, x, reference):
        with torch.no_grad():
            x_features = self.feature_extractor(x)
            reference_features = self.feature_extractor(reference)
            
            similarity = F.cosine_similarity(x_features, reference_features).mean()
            distance = abs(x_features - reference_features).mean()
            
            return abs(similarity - distance).mean()

# def diff_betweens_feature_space(video_frames, reference=None, threshold=0.997):
def diff_betweens_feature_space(video_frames, reference=None, threshold=0.84):
    model = DiffFeatureSpace(threshold)
    key_frames = []
    similaritys = []
    
    for frame in range(len(video_frames)-1):
        # Check if video_frames[frame] has 3 channels
        if video_frames[frame].shape[0] != 3:
            video_frame = torch.Tensor(video_frames[frame]).unsqueeze(0).expand(3, -1, -1).unsqueeze(0).to(model.device)
            # Convert video_frames[frame] from 2D to 3D tensor
            # video_frame = video_frames[frame].unsqueeze(0).expand(3, -1, -1)
        else:
            video_frame = torch.Tensor(video_frames[frame]).unsqueeze(0).to(model.device)
            # video_frame = video_frames[frame].unsqueeze(0)
        
        # Convert reference from 2D to 3D tensor if needed
        if reference is None:
            reference_frame = torch.Tensor(video_frames[frame + 1]).unsqueeze(0).expand(3, -1, -1).unsqueeze(0).to(model.device)
        elif reference.shape[0] != 3:
            reference_frame = torch.Tensor(reference).unsqueeze(0).expand(3, -1, -1).unsqueeze(0).to(model.device)
            # reference_frame = reference.unsqueeze(0).expand(3, -1, -1).unsqueeze(0)
        
        similarity = model.forward(video_frame, reference_frame)
        similaritys.append(similarity)

        if (similarity > threshold and similarity < 0.95) and similarity != 1.:
            key_frames.append(frame)

    if len(key_frames) <= 0:
        key_frames.append(99999)
            
    # print(f"{len(key_frames)}, {max(similaritys), min(similaritys)}")
    return key_frames, threshold, video_frames

if __name__ == "__main__":
    import numpy as np
    x = np.random.randn(1, 3, 224, 224)
    reference = np.random.randn(224, 224)
    # reference = x[0][0]
    threshold = 0.6
    list_frames = diff_betweens_feature_space(x, reference, threshold)
    print(len(list_frames))

