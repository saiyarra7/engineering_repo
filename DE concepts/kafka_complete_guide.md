
# Apache Kafka — Concepts, Architecture, and Practical Usage

## 1. What Kafka Is

Apache Kafka is a distributed event streaming platform designed for high-throughput, fault-tolerant, and scalable data pipelines and real-time applications.

Kafka fundamentally behaves as a **distributed, append-only commit log** where:
- Data is written sequentially
- Data is immutable
- Consumers control their read position

---

## 2. Core Architecture

### 2.1 Broker
A Kafka broker is a server that:
- Stores data (topic partitions)
- Handles producer writes and consumer reads

A Kafka cluster consists of multiple brokers.

---

### 2.2 Topic
A topic is a logical stream of records.

Examples:
- `user_events`
- `orders`
- `payments`

Topics are split into **partitions**.

---

### 2.3 Partition
A partition is:
- An ordered, immutable sequence of records
- The unit of parallelism
- The boundary of ordering guarantees

Ordering is guaranteed **only within a single partition**.

---

### 2.4 Offset
An offset is:
- A monotonically increasing integer
- The position of a record within a partition

Offsets are:
- Managed by consumers
- Stored internally in Kafka (`__consumer_offsets`)

---

### 2.5 Record Structure

A Kafka record contains:
- Key (optional)
- Value
- Timestamp
- Headers (optional)

---

## 3. Replication and Fault Tolerance

### 3.1 Replicas
Each partition has:
- One leader
- Zero or more followers

Only the leader:
- Accepts writes
- Serves reads (by default)

---

### 3.2 ISR (In-Sync Replicas)
ISR is the set of replicas that:
- Are fully caught up with the leader
- Can be elected leader if the current leader fails

---

### 3.3 Acknowledgements (`acks`)

Producer durability control:

| acks | Behavior |
|----|----|
| 0 | No acknowledgement |
| 1 | Leader ack only |
| all | Leader + ISR ack |

---

## 4. Producers

### 4.1 Producer Responsibilities
- Partition selection
- Batching
- Compression
- Retries
- Idempotence

---

### 4.2 Key-Based Partitioning
Records with the same key always go to the same partition.

---

### 4.3 Producer Code (Python)

```python
from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    acks='all',
    retries=3
)

producer.send(
    topic='user_events',
    key=b'user_123',
    value={'event': 'login', 'user_id': 123}
)

producer.flush()
```

---

## 5. Consumers

### 5.1 Pull-Based Model
Consumers:
- Pull data at their own pace
- Control backpressure
- Commit offsets manually or automatically

---

### 5.2 Consumer Groups
- Consumers sharing the same `group.id`
- Each partition is consumed by **only one consumer per group**
- Enables horizontal scaling

---

### 5.3 Rebalancing
Occurs when:
- A consumer joins/leaves the group
- Number of partitions changes

Rebalancing pauses consumption temporarily.

---

### 5.4 Consumer Code (Python)

```python
from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(
    'user_events',
    bootstrap_servers='localhost:9092',
    group_id='analytics_group',
    auto_offset_reset='earliest',
    enable_auto_commit=False,
    value_deserializer=lambda v: json.loads(v.decode('utf-8'))
)

for message in consumer:
    print(message.value)
    consumer.commit()
```

---

## 6. Delivery Semantics

### 6.1 At-Most-Once
- Commit offset before processing
- Possible data loss

### 6.2 At-Least-Once
- Commit offset after processing
- Possible duplicates

### 6.3 Exactly-Once
- Idempotent producers
- Transactions
- Supported in Kafka Streams and Structured Streaming

---

## 7. Retention and Storage

### 7.1 Retention Policies
- Time-based (`retention.ms`)
- Size-based (`retention.bytes`)

Kafka deletes old data regardless of consumption.

---

### 7.2 Log Compaction
Keeps only the latest record per key.

Use cases:
- User profiles
- Account state
- Configuration topics

---

## 8. Kafka as a Data Backbone

### 8.1 Decoupling Systems
Producers and consumers evolve independently.

### 8.2 Replayability
- Reprocess historical data
- Enable backfills and audits

---

## 9. Kafka vs Traditional Messaging

| Feature | Kafka | Queue Systems |
|----|----|----|
| Persistence | Yes | Often transient |
| Replay | Yes | No |
| Ordering | Per partition | Global |
| Throughput | Very high | Moderate |
| Fan-out | Native | Limited |

---

## 10. Scaling Kafka

### 10.1 Increase Partitions
Improves:
- Throughput
- Consumer parallelism

Tradeoff:
- Ordering complexity

---

### 10.2 Add Brokers
Improves:
- Storage
- Fault tolerance

---

## 11. Failure Scenarios

### 11.1 Broker Failure
- Leader election occurs
- ISR follower becomes leader

### 11.2 Consumer Failure
- Partitions reassigned
- Possible duplicate processing

### 11.3 Producer Retries
- Can cause duplicates without idempotence

---

## 12. Transactions and Idempotence

### 12.1 Idempotent Producer
Guarantees:
- No duplicate writes on retries

### 12.2 Transactions
Ensures:
- Atomic writes across partitions
- Exactly-once stream processing

---

## 13. Kafka in Data Engineering

### 13.1 Common Pipelines
- CDC → Kafka → Spark/Flink → Data Lake
- Event ingestion → Kafka → Real-time analytics

### 13.2 Spark Structured Streaming Example

```python
df = (
    spark.readStream
    .format("kafka")
    .option("kafka.bootstrap.servers", "localhost:9092")
    .option("subscribe", "user_events")
    .load()
)

parsed = df.selectExpr("CAST(value AS STRING)")
```

---

## 14. Mental Models

- Kafka is a **log**, not a queue
- Partitions define scalability and ordering
- Consumer groups define parallelism
- Offsets define progress
- Retention defines storage lifecycle

---

## 15. Common Misconceptions

- Kafka does not guarantee global ordering
- Kafka is not a database
- Kafka is not request-response
- Consumers do not delete data

---

## 16. When Kafka Is a Bad Choice

- Very low message volume
- Simple task queues
- Strict synchronous workflows
- Long-term archival storage

---

## 17. Summary

Kafka enables scalable, fault-tolerant, replayable event-driven systems by combining durable storage with high-throughput distributed messaging.
