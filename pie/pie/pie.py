import argparse
import random
import string
import tempfile
import timeit

import boto3


def calculate_pi():
    q, r, t, k, n, l = 1, 0, 1, 1, 3, 3
    while True:
        if 4 * q + r - t < n * t:
            yield n
            nr = 10 * (r - n * t)
            n = ((10 * (3 * q + r)) // t) - 10 * n
            q *= 10
            r = nr
        else:
            nr = (2 * q + r) * l
            nn = (q * (7 * k) + 2 + (r * l)) // (t * l)
            q *= k
            t *= l
            l += 2
            k += 1
            n = nn
            r = nr


def calculate_to_file(output, duration):
    start = timeit.default_timer()
    for digit in calculate_pi():
        output.write(str(digit))
        if timeit.default_timer() - start >= duration:
            break


def upload_file(path, bucket):
    s3 = boto3.resource("s3")
    key = "".join((random.choice(string.ascii_lowercase) for _ in range(42)))
    s3.meta.client.upload_file(path, bucket, key)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "duration", type=int, default=300, help="Seconds to run calculation for."
    )
    parser.add_argument("bucket", help="Name of S3 bucket to upload result to.")
    args = parser.parse_args()
    with tempfile.NamedTemporaryFile("w") as output:
        calculate_to_file(output, args.duration)
        upload_file(output.name, args.bucket)


if __name__ == "__main__":
    main()
