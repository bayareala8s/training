import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Order } from './order.entity';
import { OrderService } from '../order/order.service';
import { OrderController } from '../order/order.controller';
import { Product } from '../product/product.entity';

@Module({
  imports: [TypeOrmModule.forFeature([Order, Product])],
  providers: [OrderService],
  controllers: [OrderController],
})
export class OrderModule {}
