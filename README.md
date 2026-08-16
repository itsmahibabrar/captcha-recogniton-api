# CAPTCHA Recognition API (Proof of Concept)

![License](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)
![Throughput](https://img.shields.io/badge/Throughput-147%2B%20RPS-brightgreen.svg)
![Avg Latency](https://img.shields.io/badge/Avg%20Latency-297ms-orange.svg)
![Status](https://img.shields.io/badge/Project%20Status-PoC-yellow.svg)

This is a lightweight, high-performance **Proof of Concept (PoC)** CAPTCHA solver service built with **FastAPI**, **OpenCV**, and **ONNX Runtime**. 

The model was custom-built using a self-collected dataset and AI assistance to solve a specific domain-dependent CAPTCHA format.

---

## ⚠️ Disclaimer & Project Scope

* **Testing/Proof-of-Concept Project:** Developed as an experimental test/PoC and has **not** been evaluated or optimized for production-level critical use cases.
* **Target Specificity:** Tailored specifically for a particular target website's CAPTCHA structure. (The website link/source is intentionally omitted).
* **Fixed Resolution:** Designed exclusively to work with images of a **specific fixed dimension (160x70 pixels)**.
* **Fixed Output Length:** Supports exactly **4-digit numeric CAPTCHAs** with medium difficulty background noise/artifacts.
* **Accuracy Rate:** Overall accuracy rate is **untested / not formally benchmarked** across external datasets.

---

## 🛠️ Tech Stack

- **Framework:** FastAPI
- **Model Engine:** ONNX Runtime
- **Computer Vision:** OpenCV, Pillow
- **Data Manipulation:** NumPy
- **Server Execution:** Uvicorn

---

## 📊 Benchmark & Performance Tests

The API's throughput and latency were evaluated using an asynchronous `aiohttp` benchmarking script under high concurrency:

| Metric | Measured Result |
| :--- | :--- |
| **Total Test Requests** | 1000 |
| **Concurrency Level** | 50 concurrent connections |
| **Throughput (RPS)** | **~147.66 req/sec** |
| **Average Latency** | **~297.32 ms** |
| **Min / Max Latency** | **29.71 ms / 999.25 ms** |
| **Success Rate** | **100% (0 failed requests)** |

---

## 💻 How to Run

### 1. Installation
Clone the repository and install dependencies:
```bash
git clone [https://github.com/itsmahibabrar/captcha-recogniton-api.git](https://github.com/itsmahibabrar/captcha-recogniton-api.git)
cd captcha-recogniton-api
pip install -r requirements.txt
```
### 2. Run
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

### 3. Docs
After making it run, go to browser and then:
```http://localhost:8000/docs```

---

## Conclusion 
Author: Mahib Abrar( [itsmahibabrar](https://github.com/itsmahibabrar) )
