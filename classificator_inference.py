import gc
import torch
import json
from torch_audioset.yamnet.model import yamnet as torch_yamnet
import timm
import torch.nn as nn
import torchvision.transforms as transforms
import numpy as np
import torch.nn.functional as F


class InferenceCNN(object):
    def __init__(self):
        self.model = None
        self.image_size = None
        self.class_map = None
        self.transforms = None
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    def load_model(self, MODEL_DIR: str):
        with open(MODEL_DIR + '/' + 'description.json', 'r') as f:
            descr = json.load(f)
        self.class_map = descr["classes"]
        self.image_size = descr["img_size"]
        self.model = My_Net(descr["model_path"], len(self.class_map.keys()), descr["model_name"])
        self.model.to(self.device)
        self.model.eval()
        self.transforms = transforms.Compose([transforms.ToTensor(),
                                              transforms.Resize((self.image_size, self.image_size))])

        return descr

    def inference(self, image_list):
        image_list = [self.transforms(self.qpixmap_to_array(image)) for image in image_list]
        preds = []
        for image in image_list:
            image = image.unsqueeze(0).to(self.device)
            pred = self.model(image).to("cpu")
            del image
            torch.cuda.empty_cache()
            gc.collect()
            preds.append(pred)
        preds = F.softmax(torch.stack(preds, dim=0), dim=0)
        probs, idxs = torch.max(preds, dim=1)
        predictions = []
        for p_value, idx in zip(probs.tolist(), idxs.tolist()):
            idx = idx[0] if isinstance(idx, list) else idx
            p_value = p_value[0] if isinstance(p_value, list) else p_value
            for cls_name, cls_idx in self.class_map.items():
                if cls_idx == idx:
                    predictions.append([cls_name, p_value])
        return predictions

    def qpixmap_to_array(self, pixmap):
        size = pixmap.size()
        w = size.width()
        h = size.height()

        qimg = pixmap.toImage()
        buffer = qimg.constBits()
        buffer.setsize(w*h*3)
        img = np.ndarray(shape=(w, h, 3),
                         buffer=buffer,
                         dtype=np.uint8)
        return img


class My_Net(torch.nn.Module):
    def __init__(self, weights_path, num_classes=10, model_name='resnet50'):
        super().__init__()
        if model_name == 'yamnet':
            self.model = torch_yamnet(pretrained=False)
        else:
            self.model = timm.create_model(model_name, pretrained=False)

        if 'efficientnet' in model_name or 'yamnet' in model_name:  # Для EfficientNet есть небольшие отличия в названии слоев
            fc_inputs = self.model.classifier.in_features
            self.model.classifier = nn.Identity()
            self.model.classifier = nn.Linear(fc_inputs, num_classes)
        else:
            fc_inputs = self.model.fc.in_features
            self.model.fc = nn.Linear(fc_inputs, num_classes)
        self.model.load_state_dict(torch.load(weights_path), strict=False)
        for name, param in self.model.named_parameters():
            param.requires_grad = False

    def forward(self, x):
        x = self.model(x)
        return x


if __name__ == "__main__":
    DIR = "H:\SchebnevRadar3.5GHz//301023" #указыввается своё место хранения
    model = InferenceCNN()
    print(model.load_model(DIR))
