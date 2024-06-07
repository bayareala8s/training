import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Order } from './order.entity';
import { Product } from '../product/product.entity';

@Injectable()
export class OrderService {
  constructor(
    @InjectRepository(Order)
    private orderRepository: Repository<Order>,
    @InjectRepository(Product)
    private productRepository: Repository<Product>,
  ) {}

  findAll(): Promise<Order[]> {
    return this.orderRepository.find({ relations: ['product'] });
  }

  async findOne(id: number): Promise<Order> {
    const order = await this.orderRepository.findOneBy({ id });
    if (!order) {
      throw new NotFoundException(`Order with ID ${id} not found`);
    }
    return order;
  }

  async create(order: Order): Promise<Order> {
    const product = await this.productRepository.findOneBy({ id: order.product.id });
    if (!product) {
      throw new NotFoundException(`Product with ID ${order.product.id} not found`);
    }
    order.totalPrice = product.price * order.quantity;
    return this.orderRepository.save(order);
  }

  async update(id: number, order: Order): Promise<Order> {
    const product = await this.productRepository.findOneBy({ id: order.product.id });
    if (!product) {
      throw new NotFoundException(`Product with ID ${order.product.id} not found`);
    }
    order.totalPrice = product.price * order.quantity;
    await this.orderRepository.update(id, order);
    return this.orderRepository.findOneBy({ id });
  }

  async remove(id: number): Promise<void> {
    await this.orderRepository.delete(id);
  }
}
